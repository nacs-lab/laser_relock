#!/usr/bin/python3

import numpy as np
from uldaq import (get_daq_device_inventory, DaqDevice, AInScanFlag,
                   ScanOption, ScanStatus, create_float_buffer,
                   InterfaceType, AiInputMode, AOutFlag,
                   DigitalDirection, DigitalPortIoType, AOutScanFlag)
import re

# Constants
CURSOR_UP = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


class mcc_daq:
    def __init__(self, device_index=0):
        interface_type = InterfaceType.ANY
        devices = get_daq_device_inventory(interface_type)
        self.device_index = device_index
        self.daq_device = DaqDevice(devices[self.device_index])    
        self.descriptor = self.daq_device.get_descriptor()
        self.ai = self.analog_input(self.daq_device)
        self.dio = self.digital_io(self.daq_device)
        self.ao = self.analog_output(self.daq_device)
        # self.connect()
        
    def connect(self):
        self.daq_device.connect(connection_code=0)
        print('Connected device',self.device_index,':',self.descriptor)

    def disconnect(self):
        if self.daq_device.is_connected():
            self.daq_device.disconnect()
        self.daq_device.release()
        print('Disconnected device',self.device_index,':',self.descriptor)

    class analog_input:
        def __init__(self,daq_device):
            self.ai_device = daq_device.get_ai_device()
            self.ai_info = self.ai_device.get_info()
            self.set_params()

        def set_params(self,channels=[0],samples=100,rate=48000,triggers=1,
                range_index=7):
            self.channels = channels
            self.samples = samples
            self.rate = rate
            self.triggers = triggers
            self.input_mode = AiInputMode.DIFFERENTIAL
            self.range_index = range_index
            self.status = None
            
            low_channel,high_channel,channel_count = channel_params(self.channels)
            self.data = create_float_buffer(channel_count,
                                            self.samples*self.triggers)

            self.set_trigger()
            
        def set_trigger(self):
            trigger_type_index = 0
            trigger_types = self.ai_info.get_trigger_types()
            self.ai_device.set_trigger(trigger_types[trigger_type_index], 0,
                                       0, 0, self.samples)

        def measure(self,continuous=False):
            low_channel,high_channel,channel_count = channel_params(self.channels)
            ranges = self.ai_info.get_ranges(self.input_mode)
            flags = AInScanFlag.DEFAULT
            scan_options = (ScanOption.RETRIGGER | ScanOption.EXTTRIGGER)
            if continuous:
                scan_options = scan_options | ScanOption.CONTINUOUS
                
            self.ai_device.a_in_scan(low_channel, high_channel,
                                     self.input_mode,ranges[self.range_index],
                                     self.samples*self.triggers,self.rate,
                                     scan_options,flags,self.data)

            if not continuous:
                status = True
                while status:
                    try:
                        status,transfer_status = self.get_status()
                        index = transfer_status.current_index
                        #print(' ',end='\x1b[1K\r')
                        #print(index,end='\r')
                    except KeyboardInterrupt:
                        break

                self.ai_device.scan_stop()

        def stop(self):
            self.ai_device.scan_stop()
            

        def get_status(self):
            self.status, self.transfer_status = self.ai_device.get_scan_status()
            return self.status,self.transfer_status

        def get_index(self):
            self.get_status()
            return self.transfer_status.current_index

    class analog_output:
        def __init__(self,daq_device):
            self.ao_device = daq_device.get_ao_device()
            self.ao_info = self.ao_device.get_info()
            self.set_scan()

        def set_scan(self,channels=[0],rate=0,data=np.zeros(1),
                       continuous=True):
            self.channels = channels
            self.rate = rate
            if len(channels)>1 and (len(channels) != np.size(data,0)):
                raise RuntimeError("size(data,0) must equal number of channels")
            self.samples = data.size
            self.data = create_float_buffer(len(channels),self.samples)
            for i in range(data.size):
                self.data[i] = data[i]
                
            if continuous:
                self.scan_options = ScanOption.CONTINUOUS
            else:
                self.scan_options = ScanOption.SINGLEIO
                
            self.status = None
            
        def run(self):
            voltage_range = 1006 # 0-5V, only one for the 1408-fs-plus
            low_channel,high_channel,channel_count = channel_params(self.channels)
            flags = AOutScanFlag.DEFAULT
            sample_rate = self.ao_device.a_out_scan(low_channel, high_channel,
                                               voltage_range, self.samples,
                                               self.rate, self.scan_options,
                                                    flags, self.data)

        def stop(self):
            status = self.get_status()
            if status == ScanStatus.RUNNING:
                self.ao_device.scan_stop()
            
        def get_status(self):
            self.status, transfer_status = self.ao_device.get_scan_status()
            return self.status

        def set_single(self,channel=0,value=0.0):
            self.ao_device.a_out(channel,1006,AOutFlag.DEFAULT,float(value))
            
    class digital_io:
        def __init__(self,daq_device):
            self.dio_device = daq_device.get_dio_device()
            self.dio_info = self.dio_device.get_info()
            
        def config_port(self,port,direction):
            port = self.parse_port(port)
            direction = self.parse_direction(direction)
            self.dio_device.d_config_port(port, direction)
            #print('Configured port',port,'for direction',direction)

        def config_bit(self,port,bit,direction):
            port = self.parse_port(port)
            direction = self.parse_direction(direction)
            self.dio_device.d_config_bit(port,bit,direction)

        def bit_out(self,port,bit,value):
            port = self.parse_port(port)
            self.dio_device.d_bit_out(port,bit,value)

        def port_out(self,port,value):
            port = self.parse_port(port)
            self.dio_device.d_out(port,int(value))

        def parse_port(self,port):
            dio_info = self.dio_device.get_info()
            port_types = dio_info.get_port_types()        
            return port_types[port]

        def parse_direction(self,direction):
            if isinstance(direction,str):
                if re.search(direction.lower(),'input'):
                    direction = DigitalDirection.INPUT
                elif re.search(direction.lower(),'output'):
                    direction = DigitalDirection.OUTPUT                    
                else:
                    raise RuntimeError('direction must be in or out')
            elif isinstance(direction,bool):
                direction = (DigitalDirection.OUTPUT if direction
                             else DigitalDirection.INPUT)
            else:
                raise RuntimeError('invalid data type for direction')

            return direction

def channel_params(channels):
    low_channel = min(channels)
    high_channel = max(channels)
    channel_count = high_channel - low_channel + 1
    return low_channel,high_channel,channel_count
