#!/usr/bin/python3

stokes = {
    'laser_type' : 'toptica',
    'wm_freq' : 472166,
    'wm_file' : '/mnt/wavemeter/20210111.csv',
    'daq_device' : 0,
    'lock_port' : 'B',
    'lock_bit' : 0,
    'ramp_chn' : 0,
    'trig_chn' : 1,
    'errsig_chn' : 0,
    'dlc_ip' : '192.168.0.205'
}

pump = {
    'laser_type' : 'homebuilt',
    'wm_freq' : 325130,
    'wm_file' : '/mnt/wavemeter/20210111.csv',
    'daq_device' : 1
    'lock_port' : 'B',
    'lock_bit' : 0,
    'ramp_chn' : 0,
    'trig_chn' : 1,
    'errsig_chn' : 0,
    'vendor' : 1510,
    'product' : 8704
}
