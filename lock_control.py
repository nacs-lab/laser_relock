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
import lock_control_settings 

class lock_control:
    def __init__(self,laser_name="stokes"):

        settings = getattr(lock_control_settings,laser_name)
        for name,value in settings.items():
            setattr(self,name,value)
        
        if self.laser_type is 'toptica':
            self.laser = toptica_laser(self.dlc_ip)
        elif self.laser_type is 'homebuilt':
            self.laser = homebuilt_laser(self.vendor,self.product)
        else:
            raise Exception("not a known laser type")
        
        self.daq = mcc_daq(self.daq_device)
        self.wm_parser = WavemeterParser(self.wm_freq-1000,self.wm_freq+1000)
        
        self.lock_state = None
        self.ramp_state = None

    def daq_connect(self):
        if not self.daq.daq_device.is_connected():
            self.daq.daq_device.connect()

    def errsig_data(self):
        result = np.zeros(self.daq.ai.data.__len__())
        result[0:] = self.daq.ai.data[0:]
        return result

    def errsig_measure(self,continuous=False,exttrigger=True):
        samples = int(self.errsig_tmax * self.errsig_sample_rate)
        self.daq_connect()
        self.daq.ai.set_params(channels=[self.errsig_chn],
                               rate=self.errsig_sample_rate,samples=samples)
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
        self.daq_connect()
        self.daq.dio.config_port(self.lock_port,'out')
        self.daq.dio.bit_out(self.lock_port,self.lock_bit,state)

    def ramp_set(self,state=True):
        self.ramp_state = bool(state)
        self.daq_connect()
        
        t = np.arange(0,self.ramp_tmax,1.0/self.ramp_sample_rate)
        trig_data = 2.5*(signal.square(2*np.pi*self.ramp_freq*t,0.1)+1.0)
        if state:
            ramp_data = self.ramp_amp*(signal.sawtooth(
                2*np.pi*self.ramp_freq*t)+1.0)
        else:
            ramp_data = 0.0 * t
                
        data = np.concatenate((trig_data[:,None],ramp_data[:,None]),axis=1)
        data = np.reshape(data,(2*len(t),))
        
        self.daq.ao.stop()
        chns = [self.trig_chn,self.ramp_chn]
        self.daq.ao.set_scan(channels=chns,rate=self.ramp_sample_rate,
                             data=data,continuous=True)
        self.daq.ao.run()
        
    def wm_read(self,duration=20):
        now = calendar.timegm(time.localtime())
        times,freqs = self.wm_parser.parse(self.wm_file,now-duration,now)
        try:
            result = freqs[-1]
        except IndexError:
            result = -1
        return result

def main():
    lc = lock_control('stokes')

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
    lc.errsig_measure(continuous=False,exttrigger=False)
    errsig_data = lc.errsig_data()
    print(errsig_data)
    
    print('not ramping:')
    lc.ramp_set(0)
    time.sleep(1)

    
    
if __name__=="__main__":
    main()
