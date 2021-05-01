#!/usr/bin/python3

'''
Class for remotely controlling & relocking nacs 1.5 stirap lasers
'''

# reading wavemeter
from libnacs.wavemeter import WavemeterParser
import time,calendar
import array as arr

# toptica laser control
import toptica.lasersdk.dlcpro.v2_1_0 as topt

# mcc daq control
from mcc_daq import mcc_daq

# constants
DLC_IP = '192.168.0.205'
LASER_FREQ = 472114
WM_FILE = '/mnt/wavemeter/20210111.csv';

class lock_control:
    def __init__(self,dlc_ip=DLC_IP,laser_freq=LASER_FREQ,wm_file=WM_FILE):
        self.dlc = topt.DLCpro(topt.NetworkConnection(dlc_ip))
        self.daq = mcc_daq(0)
        self.wm = WavemeterParser(laser_freq-1000,laser_freq+1000)

    def lock(self):
        self;
    def ramp(self):
        self;
    def read_wm(self,duration=0):
        self;
