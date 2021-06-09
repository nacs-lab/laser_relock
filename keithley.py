#!/usr/bin/python3

import usbtmc

VENDOR = 1510
PRODUCT = 8704

class keithley:
    def __init__(self,vendor=VENDOR,product=PRODUCT):
        self.vendor = vendor
        self.product = product
        self.connect()
        self.VoltageLimit = 10.0
        self.CurrentLimit = 1.0
        self.Voltage = self.getVoltage()
        self.Current = self.getCurrent()
        
    def connect(self):
        self.inst = usbtmc.Instrument(VENDOR,PRODUCT)
        self.inst.open()
        self.set_remote()
        
    def set_remote(self):
        self.inst.write('SYST:REM')
        
    def close(self):
        self.inst.close()
    
    def getCurrent(self):
        self.Current = float(self.inst.ask('SOUR:CURR:LEV?'))
        return self.Current
        
    def getVoltage(self):
        self.Voltage = float(self.inst.ask('SOUR:VOLT:LEV?'))
        return self.Voltage
    
    def measureVoltage(self):
        res = float(self.inst.ask('MEAS:VOLT?'))
        return res
    
    def measureCurrent(self):
        res = float(self.inst.ask('MEAS:CURR?'))
        return res
        
    def getIDN(self):
        return self.inst.ask("*IDN?")
    
    def setCurrent(self,current):
        if (current > self.CurrentLimit) or (current < 0.0):
            raise Exception("current out of range")
        self.inst.write('SOUR:CURR:LEV %.3f\n' % current)
        
    def setVoltage(self,voltage):
        if (abs(voltage) > self.VoltageLimit) or abs(voltage) > 30.0:
            raise Exception("voltage out of range")
        self.inst.write('SOUR:VOLT:LEV %.3f\n' % voltage)
        
    def setOutput(self,output):
        self.inst.write('SOUR:OUTP:STAT %.3f\n' % output)

