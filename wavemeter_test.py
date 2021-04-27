#!/usr/bin/python

from libnacs.wavemeter import WavemeterParser
import time,calendar
import array as arr

date = '20180202_170922';
duration = 100;
f = '/mnt/wavemeter/20210111.csv';


wm = WavemeterParser(350000, 352000);

now = calendar.timegm(time.localtime())

times,freqs = wm.parse(f,now-20,now)

print(times)
print(freqs)

