#!/usr/bin/python3

'''
Class for remotely controlling & relocking nacs 1.5 stirap lasers
'''

# reading wavemeter
from libnacs.wavemeter import WavemeterParser
import time,calendar

# toptica laser control
from toptica.lasersdk.dlcpro.v2_1_0 import DLCpro, NetworkConnection

# mcc daq control
from mcc_daq import mcc_daq
from scipy import signal
import numpy as np

# constants
DLC_IP = '192.168.0.205'
#WM_FREQ = 472176
WM_FREQ = 288584
WM_FILE = '/mnt/wavemeter/20210111.csv'
DAQ_DEVICE = 0

class lock_control:
    def __init__(self,daq_device = DAQ_DEVICE):
        self.laser = self._laser()
        self.daq = mcc_daq(0)
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

        def measure(self,continuous=False,tmax=0.1,rate=4800,channel=0):
            self.__owner.daq_connect()
            samples = int(tmax * rate)
            self.__owner.daq.ai.set_params(channels=[channel],rate=rate,
                                           samples=samples)
            self.__owner.daq.ai.measure(continuous=continuous)

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
            
        def set(self,state=0,port=0,bit=0):
            self.state = bool(state)
            self.__owner.daq_connect()
            self.__owner.daq.dio.bit_out(port,bit,state)

    class _ramp:
        def __init__(self,owner,offs=2.5,amp=2.5):
            self.state = None
            self.__owner = owner
            self.offs = offs
            self.amp = amp
            self.set()
        
        def set(self,state=True,freq=100.0,rate=1000.0,
                tmax=1.0,channel=0):
            self.state = bool(state)
            self.__owner.daq_connect()
            if state:
                t = np.arange(0,tmax,1.0/rate)
                data = self.amp * signal.sawtooth(2 * np.pi * freq * t,0.5) + self.offs
                self.__owner.daq.ao.set_scan(channels=[channel],rate=rate,
                                             data=data,continuous=True)
                self.__owner.daq.ao.run()
            else:
                self.__owner.daq.ao.stop()
            
            
    class _wm:
        def __init__(self,wm_freq=WM_FREQ,wm_file=WM_FILE):
            self.parser = WavemeterParser(wm_freq-1000,wm_freq+1000)
            self.filename = wm_file
        def read(self,duration=20):
            now = calendar.timegm(time.localtime())
            times,freqs = self.parser.parse(self.filename,now-duration,now)
            return freqs[-1]

    class _laser:
        def __init__(self,dlc_ip=DLC_IP):
            self.dlc = DLCpro(NetworkConnection(dlc_ip))
            self.current = self.read_current()
            self.piezo = self.read_piezo()
            
        def read_current(self):
            with self.dlc as dlc:
                self.current = dlc.laser1.dl.cc.current_set.get()
            return self.current
        
        def set_current(self,current):
            with self.dlc as dlc:
                if current:
                    dlc.laser1.dl.cc.current_set.set(current)
            return self.read_current()
        
        def read_piezo(self):
            with self.dlc as dlc:
                self.piezo_voltage = dlc.laser1.dl.pc.voltage_set.get()
            return self.piezo_voltage
        
        def set_piezo(self,piezo):
            with self.dlc as dlc:
                if piezo:
                    dlc.laser1.dl.pc.voltage_set.set(piezo)
            return self.read_piezo()
    

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
    for i in range(10):
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
