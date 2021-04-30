#!/usr/bin/python3

import numpy as np
from mcc_daq import mcc_daq
import time

daq = mcc_daq(0)

data = np.zeros(100)

daq.ao.set_scan(channels=[0],rate=100,data=data,continuous=True)

daq.ao.run()

print(daq.ao.get_status())

time.sleep(1)

daq.ao.stop()

print(daq.ao.get_status())

daq.disconnect()

