#!/usr/bin/python3

from numpy import reshape
from uldaq import (get_daq_device_inventory, DaqDevice, AInScanFlag,
                   ScanOption, ScanStatus, create_float_buffer,
                   InterfaceType, AiInputMode)

class mcc_daq:
    def __init__(self, device_index=0):
        interface_type = InterfaceType.ANY
        devices = get_daq_device_inventory(interface_type)
        self.daq_device = DaqDevice(devices[device_index])    
        self.descriptor = self.daq_device.get_descriptor()
        self.ai = self.analog_input(self.daq_device)
        self.connect()
        print('Connected to',self.descriptor)
        
    def connect(self):
        self.daq_device.connect(connection_code=0)

    def disconnect(self):
        if self.daq_device.is_connected():
            self.daq_device.disconnect()
        self.daq_device.release()

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
            
            low_channel,high_channel,channel_count = self.channel_params()
            self.data = create_float_buffer(channel_count,
                                            self.samples*self.triggers)

            self.set_trigger()
            
        def set_trigger(self):
            trigger_type_index = 0
            trigger_types = self.ai_info.get_trigger_types()
            self.ai_device.set_trigger(trigger_types[trigger_type_index], 0,
                                       0, 0, self.samples)

        def measure(self,continuous=False):
            low_channel,high_channel,channel_count = self.channel_params()
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
            
        def channel_params(self):
            low_channel = min(self.channels)
            high_channel = max(self.channels)
            channel_count = high_channel - low_channel + 1
            return low_channel,high_channel,channel_count

        def get_status(self):
            self.status, transfer_status = self.ai_device.get_scan_status()
            return self.status,transfer_status
