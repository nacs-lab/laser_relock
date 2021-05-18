#!/usr/bin/python3

class laser_settings:
    laser_type = None
    wm_freq = None
    wm_file = None
    daq_device = None

stokes = laser_settings()
stokes.laser_type = 'toptica'
stokes.wm_freq = 472166
stokes.wm_file = '/mnt/wavemeter/20210111.csv'
stokes.daq_device = 0

pump = laser_settings()
pump.laser_type = 'homebuilt'
pump.wm_freq = 325130
pump.wm_file = '/mnt/wavemeter/20210111.csv'
pump.daq_device = 1
