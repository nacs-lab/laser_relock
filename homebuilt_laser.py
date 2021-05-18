#!/usr/bin/python3

from keithley import keithley

class homebuilt_laser:
        def __init__(self,dlc_ip=DLC_IP):
            self.keithley = keithley()
            self.current = self.read_current()
            self.piezo = self.read_piezo()
            
        def read_current(self):
            return -1
        
        def set_current(self,current):
            return -1
        
        def read_piezo(self):
            return self.keithley.getVoltage()
        
        def set_piezo(self,piezo):
            return self.keithley.setVoltage(piezo)
