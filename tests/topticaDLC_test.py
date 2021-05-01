#!/usr/bin/python3

from toptica.lasersdk.dlcpro.v2_0_3 import DLCpro, NetworkConnection

ip = '192.168.0.205'


class someclass:
    def __init__(self):
        self.dlc = DLCpro(NetworkConnection(ip))
    def read_voltage(self):
        self.dlc.laser1.dl.pc.voltage_set.get()

laser = someclass()
with laser.dlc as dlc:
    print(dlc.laser1.dl.pc.voltage_set.get())    
#laser.read_voltage()
        


with DLCpro(NetworkConnection(ip)) as dlc:
    # print(dlc.uptime_txt.get())
    # print(dlc.system_label.get())

    #print("\n\n=== Sync Read ===\n")
    #print('     System Time :', dlc.time.get())
    #print('          Uptime :', dlc.uptime.get())
    #print('Firmware Version :', dlc.fw_ver.get())
    #print('   System Health :', dlc.system_health_txt.get())
    #print('        Emission :', dlc.emission.get())
    #print('  Scan Frequency :', dlc.laser1.scan.frequency.get())
    print(dlc.laser1.dl.pc.voltage_set.get())
    # dlc.laser1.dl.cc.current_set.set(126.0514)
    print(dlc.laser1.dl.cc.current_set.get())
    #print(dlc.laser1.dl.cc


