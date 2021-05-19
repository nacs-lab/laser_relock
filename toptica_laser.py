#!/usr/bin/python3

# toptica laser control
from toptica.lasersdk.dlcpro.v2_1_0 import DLCpro, NetworkConnection

class toptica_laser:
        def __init__(self,dlc_ip):
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
        
        def read_piezo(self):
            with self.dlc as dlc:
                self.piezo_voltage = dlc.laser1.dl.pc.voltage_set.get()
            return self.piezo_voltage
        
        def set_piezo(self,piezo):
            with self.dlc as dlc:
                if piezo:
                    dlc.laser1.dl.pc.voltage_set.set(piezo)
