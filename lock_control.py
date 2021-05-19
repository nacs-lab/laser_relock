#!/usr/bin/python3

'''
Class for remotely controlling & relocking nacs 1.5 stirap lasers
'''

# reading wavemeter
from libnacs.wavemeter import WavemeterParser
import time,calendar

# toptica laser control
from toptica_laser import toptica_laser
from homebuilt_laser import homebuilt_laser

# mcc daq control
from mcc_daq import mcc_daq
from scipy import signal
import numpy as np

# setting
import laser_settings
ERRSIG_SAMPLE_RATE = 48000
RAMP_SAMPLE_RATE = 50000
RAMP_AMP = 0.1
RAMP_OFFS = 0.0

class lock_control:
    def __init__(self,laser_name="pump"):
        self.settings = getattr(laser_settings,laser_name)
        if (self.settings['laser_type'] == 'toptica'):
            self.laser = toptica_laser(self.settings['dlc_ip'])
        elif (self.settings['laser_type'] == 'homebuilt'):
            self.laser = homebuilt_laser(self.settings['vendor'],
                                         self.settings['product'])
        else:
            raise Exception("not a known laser type")
        self.daq = mcc_daq(self.settings['daq_device'])
        self.wm_parser = WavemeterParser(self.settings['wm_freq']-1000,self.settings['wm_freq']+1000)
        self.lock_state = None
        self.ramp_state = None
        self.ramp_amp = None
        self.ramp_freq = None
        self.ramp_offs = None

    def daq_connect(self):
        if not self.daq.daq_device.is_connected():
            self.daq.daq_device.connect()

    def errsig_data(self):
        result = np.zeros(self.daq.ai.data.__len__())
        result[0:] = self.daq.ai.data[0:]
        return result

    def errsig_measure(self,continuous=False,tmax=0.01,
                       rate=48000,exttrigger=True):
        channel = self.settings['errsig_chn']
        self.daq_connect()
        samples = int(tmax * rate)
        self.daq.ai.set_params(channels=[channel],rate=rate,
                                        samples=samples)
        self.daq.ai.measure(continuous=continuous,exttrigger=exttrigger)

    def errsig_get_status(self):
        status,other = self.daq.ai.get_status()
        return str(status)

    def errsig_get_index(self):
        return int(self.daq.ai.get_index())

    def errsig_stop(self):
        self.daq.ai.stop()
                
    def lock_set(self,state=0):
        self.lock_state = bool(state)
        port = self.settings['lock_port']
        bit = self.settings['lock_bit']
        self.daq_connect()
        self.daq.dio.config_port(port,'out')
        self.daq.dio.bit_out(port,bit,state)

    def ramp_set(self,state=True,freq=50.0,rate=50000.0,tmax=0.05):
        self.ramp_state = bool(state)
        self.daq_connect()
        
        t = np.arange(0,tmax,1.0/rate)
        trig_data = 2.5 * (signal.square(2 * np.pi * freq * t,0.1) + 1.0)
        if state:
            ramp_data = self.ramp_amp*(signal.sawtooth(2*np.pi*freq*t,
                                                       0.5)+1.0)
        else:
            ramp_data = 0.0 * t
                
        data = np.concatenate((trig_data[:,None],ramp_data[:,None]),axis=1)
        data = np.reshape(data,(2*len(t),))
        
        self.daq.ao.stop()
        chns = [self.settings['trig_chn'],self.settings['ramp_chn']]
        self.daq.ao.set_scan(channels=chns,rate=rate,
                             data=data,continuous=True)
        self.daq.ao.run()
        
    def wm_read(self,duration=20):
        now = calendar.timegm(time.localtime())
        times,freqs = self.parser.parse(self.filename,
                                        now-duration,now)
        try:
            result = freqs[-1]
        except IndexError:
            result = -1
        print(result)
        return result

def main():
    lc = lock_control()

    print('reading current:')
    current = lc.laser.read_current()
    print(current)

    print('setting current')
    current = lc.laser.set_current(current + 0.0001)
    print(current)
    
    print('reading piezo:')
    piezo = lc.laser.read_piezo()
    print(piezo)

    print('setting piezo:')
    piezo = lc.laser.set_piezo(piezo + 0.00001)
    print(piezo)

    print('reading wavemeter:')
    for i in range(3):
        wl = lc.wm_read()
        print(wl)
        time.sleep(1)

    print('engaging lock:')
    lc.lock_set(1)
    time.sleep(1)

    print('disengaging lock')
    lc.lock_set(0)

    print('ramping:')
    lc.ramp_set(1)

    print('measuring error signal:')
#    lc.errsig.measure
    
    print('not ramping:')
    lc.ramp.set(0)
    time.sleep(1)

    
    
if __name__=="__main__":
    main()
