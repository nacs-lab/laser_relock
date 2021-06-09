#!/usr/bin/python3

from mcc_daq import mcc_daq

daq = [mcc_daq(i) for i in range(2)]

[daq[i].connect() for i in range(2)]

[daq[i].dio.config_port(1,'out') for i in range(2)]

print(' ')
print('testing digital output channels')
for i in range(2):
    print(' ')
    print('setting channel %d high' % i)
    daq[i].dio.bit_out(1,0,1)
    print('settings channel %d low' % int(not i))
    daq[int(not i)].dio.bit_out(1,0,0)

    daq[i].ai.set_params(channels=[0],samples=1,rate=48,triggers=1,range_index=1)
    daq[i].ai.measure(continuous=False,exttrigger=False)

    daq[int(not i)].ai.set_params(channels=[0],samples=1,
                                  rate=48,triggers=1)
    daq[int(not i)].ai.measure(continuous=False,exttrigger=False)

    print('high chn (%d) measurement:' % i)
    print(daq[i].ai.data[0])

    print('low chn (%d) measurement:' % int(not i))
    print(daq[int(not i)].ai.data[0])

    daq[i].dio.port_out(1,0)
    daq[int(not i)].dio.port_out(1,0)


    
print(' ')
print('testing analog output channels')
for i in range(2):
    print(' ')
    print('setting channel %d high' % i)
    daq[i].ao.set_single(1,4.5)
    print('settings channel %d low' % int(not i))
    daq[int(not i)].ao.set_single(1,0.5)

    daq[i].ai.set_params(channels=[0],samples=1,rate=48,triggers=1,range_index=1)
    daq[i].ai.measure(continuous=False,exttrigger=False)

    daq[int(not i)].ai.set_params(channels=[0],samples=1,
                                  rate=48,triggers=1)
    daq[int(not i)].ai.measure(continuous=False,exttrigger=False)

    print('high chn (%d) measurement:' % i)
    print(daq[i].ai.data[0])

    print('low chn (%d) measurement:' % int(not i))
    print(daq[int(not i)].ai.data[0])



