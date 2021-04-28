#!/usr/bin/python 

from time import sleep
from os import system
import numpy as np
import matplotlib.pyplot as plt

from uldaq import (get_daq_device_inventory, DaqDevice, AInScanFlag,    
                   ScanOption, ScanStatus, create_float_buffer,         
                   InterfaceType, AiInputMode)                          

def main():
    daq_device = None
    ai_device = None
    status = 1;

    range_index = 7
    trigger_type_index = 0
    interface_type = InterfaceType.ANY
    low_channel = 0
    high_channel = 0
    descriptor_index = 0
    samples_per_channel = 1000
    samples_per_trigger = 1000
    sample_rate = 48000
    input_mode = AiInputMode.DIFFERENTIAL
    scan_options = ScanOption.RETRIGGER | ScanOption.EXTTRIGGER | ScanOption.DEFAULTIO
    flags = AInScanFlag.DEFAULT
    
    try:
        devices = get_daq_device_inventory(interface_type)
        number_of_devices = len(devices)

        daq_device = DaqDevice(devices[descriptor_index])

        ai_device = daq_device.get_ai_device()
        
        ai_info = ai_device.get_info()
        
        descriptor = daq_device.get_descriptor()

        daq_device.connect(connection_code=0)
        
        number_of_channels = ai_info.get_num_chans_by_mode(input_mode)
        channel_count = high_channel - low_channel + 1
        
        ranges = ai_info.get_ranges(input_mode)

        trigger_types = ai_info.get_trigger_types()
        
        ai_device.set_trigger(trigger_types[trigger_type_index], 0,
                              0, 0, samples_per_trigger)
        
        data = create_float_buffer(channel_count, samples_per_channel)

        ai_device.a_in_scan(low_channel, high_channel, input_mode,
                            ranges[range_index], samples_per_channel, sample_rate,
                            scan_options, flags, data)

        n=1
        while status:
            try:
                status, transfer_status = ai_device.get_scan_status()
                index = transfer_status.current_index
                system('clear')
                print(index)
                print(n)
                n=n+1
            except (ValueError, NameError, SyntaxError):
                break
    
    except RuntimeError as error:
        print('\n', error)

    finally:
        if daq_device:
            # Stop the acquisition if it is still running.
            if status == ScanStatus.RUNNING:
                ai_device.scan_stop()
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()


    dt = 1/sample_rate
    t = dt * np.arange(samples_per_channel)
    plt.plot(t,data)
    plt.show()

if __name__ == '__main__':
    main()
