#!/usr/bin/python3

from mcc_daq import mcc_daq

daq = mcc_daq(0)

# daq.ai.set_params(rate=100,samples=100)

# daq.ai.measure()

daq.dio.config_port(0,True)

daq.dio.port_out(0,255)

daq.disconnect()


