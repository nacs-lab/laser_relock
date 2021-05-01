#!/usr/bin/python

from libnacs.wavemeter import WavemeterParser
import time,calendar
import array as arr

duration = 100;
f = '/mnt/wavemeter/20210111.csv';

wm = WavemeterParser(472000, 473000);

now = calendar.timegm(time.localtime())

times,freqs = wm.parse(f,now-20,now)

print(times)
print(freqs)

