#!/usr/bin/python3

'''
Class for remotely controlling & relocking nacs 1.5 stirap lasers
'''
# reading wavemeter
from libnacs.wavemeter import WavemeterParser
import time,calendar

# toptica laser control
from toptica_laser import toptica_laser

# mcc daq control
from mcc_daq import mcc_daq
from scipy import signal
import numpy as np

# constants
WM_FREQ = 472166
#WM_FREQ = 288584
WM_FILE = '/mnt/wavemeter/20210111.csv'
DAQ_DEVICE = 0

class lock_control:
    def __init__(self,daq_device = DAQ_DEVICE):
        self.laser = toptica_laser()
        self.daq = mcc_daq(daq_device)
        self.wm = self._wm()
        self.lock = self._lock(self)
        self.ramp = self._ramp(self)
        self.errsig = self._errsig(self)

    def delete(self):
        if self.daq.daq_device.is_connected():
            self.daq.disconnect()

    def daq_connect(self):
        if not self.daq.daq_device.is_connected():
            self.daq.daq_device.connect()

    class _errsig:
        def __init__(self,owner):
            self.__owner = owner

        def data(self):
            result = np.zeros(self.__owner.daq.ai.data.__len__())
            result[0:] = self.__owner.daq.ai.data[0:]
            return result

        def measure(self,continuous=False,tmax=0.01,rate=48000,
                    channel=0,exttrigger=True):
            self.__owner.daq_connect()
            samples = int(tmax * rate)
            self.__owner.daq.ai.set_params(channels=[channel],rate=rate,
                                           samples=samples)
            self.__owner.daq.ai.measure(continuous=continuous,exttrigger=exttrigger)

        def get_status(self):
            status,other = self.__owner.daq.ai.get_status()
            return str(status)

        def get_index(self):
            return int(self.__owner.daq.ai.get_index())

        def stop(self):
            self.__owner.daq.ai.stop()
        
    class _lock:
        def __init__(self,owner):
            self.state = None
            self.__owner = owner
            
        def set(self,state=0,port=1,bit=0):
            self.state = bool(state)
            self.__owner.daq_connect()
            self.__owner.daq.dio.config_port(port,'out')
            self.__owner.daq.dio.bit_out(port,bit,state)

    class _ramp:
        def __init__(self,owner,offs=2.5,amp=0.1):
            self.state = None
            self.__owner = owner
            self.offs = offs
            self.amp = amp
            self.set()
        
        def set(self,state=True,freq=50.0,rate=50000.0,
                tmax=0.05,channel=1):
            self.state = bool(state)
            self.__owner.daq_connect()

            
            #if state:
            #    amp1 = self.amp
            #else:
            #    amp1 = 0.0

            amp1 = self.amp
            t = np.arange(0,tmax,1.0/rate)
            if state:        
                
                #data1 = amp1 * signal.sawtooth(2 * np.pi * freq * t,0.5) + self.offs
                data1 = amp1 * signal.sawtooth(2 * np.pi * freq * t,0.5) + amp1
            else:
                data1 = 0.0 * t
            data0 = 2.5 * (signal.square(2 * np.pi * freq * t,0.1) + 1.0)
                
            data = np.concatenate((data0[:,None],data1[:,None]),axis=1)
            data = np.reshape(data,(2*len(t),))
                
            self.__owner.daq.ao.stop()
            self.__owner.daq.ao.set_scan(channels=[0,1],rate=rate,
                                         data=data,continuous=True)
            self.__owner.daq.ao.run()

            
            
    class _wm:
        def __init__(self,wm_freq=WM_FREQ,wm_file=WM_FILE):
            self.parser = WavemeterParser(wm_freq-1000,wm_freq+1000)
            self.filename = wm_file
        def read(self,duration=20):
            now = calendar.timegm(time.localtime())
            times,freqs = self.parser.parse(self.filename,now-duration,now)
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
