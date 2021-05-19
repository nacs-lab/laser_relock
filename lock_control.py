#!/usr/bin/python3

'''
Class for remotely controlling & relocking nacs 1.5 stirap lasers
'''

# reading wavemeter
#from libnacs.wavemeter import WavemeterParser
from wavemeter import wavemeter
import time,calendar

# toptica laser control
from toptica_laser import toptica_laser
from homebuilt_laser import homebuilt_laser

# mcc daq control
from mcc_daq import mcc_daq
from scipy import signal
import numpy as np

import laser_settings

class lock_control:
    def __init__(self,laser_name="pump"):
        self.settings = getattr(laser_settings,laser_name)
        if (self.settings.laser_name == 'toptica'):
            self.laser = toptica_laser()
        elif (self.settings.laser_name == 'homebuilt'):
            self.laser = homebuilt_laser()
        else:
            raise Exception("not a known laser type")
        self.daq = mcc_daq(self.settings.daq_device)
        self.parser = WavemeterParser(self.settings.wm_freq-1000,self.settings.wm_freq+1000)

    def daq_connect(self):
        if not self.daq.daq_device.is_connected():
            self.daq.daq_device.connect()

    def errsig_data(self):
        result = np.zeros(self.daq.ai.data.__len__())
        result[0:] = self.daq.ai.data[0:]
        return result

    def errsig_measure(self,continuous=False,tmax=0.01,rate=48000,
                channel=0,exttrigger=True):
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
                
    def lock_set(self,state=0,port=1,bit=0):
        self.state = bool(state)
        self.daq_connect()
        self.daq.dio.config_port(port,'out')
        self.daq.dio.bit_out(port,bit,state)

    def ramp_set(self,state=True,freq=50.0,rate=50000.0,
                 tmax=0.05,channel=1):
        self.state = bool(state)
        self.daq_connect()
        
        amp1 = self.amp
        t = np.arange(0,tmax,1.0/rate)
        if state:        
            data1 = amp1*signal.sawtooth(2*np.pi*freq*t,0.5)+amp1
        else:
            data1 = 0.0 * t
        data0 = 2.5 * (signal.square(2 * np.pi * freq * t,0.1) + 1.0)
                
        data = np.concatenate((data0[:,None],data1[:,None]),axis=1)
        data = np.reshape(data,(2*len(t),))
                
        self.daq.ao.stop()
        self.daq.ao.set_scan(channels=[0,1],rate=rate,
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
        wl = lc.wm.read()
        print(wl)
        time.sleep(1)

    print('engaging lock:')
    lc.lock.set(1)
    time.sleep(1)

    print('disengaging lock')
    lc.lock.set(0)

    print('ramping:')
    lc.ramp.set(1)

    print('measuring error signal:')
#    lc.errsig.measure
    
    print('not ramping:')
    lc.ramp.set(0)
    time.sleep(1)

    
    
if __name__=="__main__":
    main()
