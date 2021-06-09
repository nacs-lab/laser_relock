#!/usr/bin/python3

from mcc_daq import mcc_daq

daq = [mcc_daq(i) for i in range(2)]

[daq[i].connect() for i in range(2)]

#[daq[i].dio.config_port(1,'out') for i in range(2)]




