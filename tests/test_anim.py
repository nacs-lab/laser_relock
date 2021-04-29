#!/usr/bin/python3

# import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys

x = np.linspace(0, 10*np.pi, 100)
phase = 0
y = np.sin(0.5 * x + phase)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'b-')

def on_close(event):
    print('figured closed.')
    sys.exit(0)

fig.canvas.mpl_connect('close_event', on_close)

try:
    while True:
        phase = phase + 0.1*np.pi
        line1.set_ydata(np.sin(0.5 * x + phase))
        fig.canvas.draw()
        plt.pause(0.0001)
except KeyboardInterrupt:
    sys.exit(0)
