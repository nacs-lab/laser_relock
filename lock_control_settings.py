#!/usr/bin/python3

defaults = {
    'wm_file' : '/mnt/wavemeter/20210111.csv',
    'ramp_amp' : 0.1,
    'ramp_freq' : 100,
    'ramp_offs' : 0.0,
    'ramp_tmax' : 0.1,
    'ramp_sample_rate' : 50000,
    'errsig_sample_rate' : 48000,
    'errsig_tmax' : 0.005,
}

stokes = {
    'laser_type' : 'toptica',
    'dlc_ip' : '192.168.0.205',
    'wm_freq' : 472166,
    'daq_device' : 0,
    'lock_port' : 1, # 0=A, 1=B
    'lock_bit' : 0,
    'trig_chn' : 1,
    'errsig_chn' : 0,
    'ramp_chn' : 0,
}
stokes.update(defaults)

pump = {
    'laser_type' : 'homebuilt',
    'wm_freq' : 325130,
    'daq_device' : 1,
    'vendor' : 1510,
    'product' : 8704,
    'lock_port' : 1, # 0=A, 1=B
    'lock_bit' : 0,
    'trig_chn' : 1,
    'errsig_chn' : 0,
    'ramp_chn' : 0,
}
pump.update(defaults)
