#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

class anim_sine:
    def __init__(self):
        self.x = np.linspace(0, 10*np.pi, 100)
        self.phase = 0
        self.y = np.sin(0.5 * self.x + self.phase)
        self.plot = plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.line1, = self.ax.plot(self.x, self.y, 'b-')
        self.isStopped = False

    def animate(self):
        self.draw_frame()
        self.after(100, self.animate)

    def draw_frame(self):
        self.phase = self.phase + 0.1*np.pi
        self.line1.set_ydata(np.sin(0.5 * self.x + self.phase))
        self.fig.canvas.draw()

p = anim_sine()
p.animate()

