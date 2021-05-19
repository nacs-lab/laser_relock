#!/usr/bin/python3

from keithley import keithley

VENDOR = 1510
PRODUCT = 8704

class homebuilt_laser:
        def __init__(self,vendor=VENDOR,product=PRODUCT):
            self.keithley = keithley(vendor,product)
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
