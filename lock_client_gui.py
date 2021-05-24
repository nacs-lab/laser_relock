#!/usr/bin/python3

import tkinter as tk
from NumericEntry import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
from lock_control_client import lock_control_client
import time

class window2:
    def __init__(self, master1):

        if len(sys.argv) > 1:
            self.laser_name = sys.argv[1]
            print('laser name: %s' % self.laser_name)
        else:
            self.laser_name = 'pump'
            print('using default laser: %s' % self.laser_name)

        self.client = lock_control_client(self.laser_name)
        self.root = master1
        self.sleepTime = 10
        self.now = time.time()

        # initialize plot
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.line, = self.ax1.plot(self.get_errsig())
        self.canvas = FigureCanvasTkAgg(self.fig,master=self.root)
        self.canvas.get_tk_widget().grid()
        self.ax1.set_ylim([-0.25,0.25])

        # lower frame with numbers & buttons
        self.panel2 = tk.Frame(self.root)
        self.panel2.grid()
        
        # numeric entries
        self.current = NumericEntryLabeled(self.root,self.panel2,self.get_current,
                                           self.set_current,label="Current")
        self.current.grid(row=0,column=0)

        self.piezo = NumericEntryLabeled(self.root,self.panel2,self.get_piezo,
                                         self.set_piezo,label="Piezo")
        self.piezo.grid(row=1,column=0)

        self.wavelength = NumericEntryLabeled(self.root,self.panel2,
                                              self.get_wavelength,
                                              self.do_nothing,label="Freq")
        self.wavelength.grid(row=0,column=1)

        self.ramp_amp = NumericEntryLabeled(self.root,self.panel2,self.get_ramp_amp,
                                     self.set_ramp_amp,label="RampAmp")
        self.ramp_amp.grid(row=1,column=1)

        # lock, quit buttons
        self.lock_btn = tk.Button(self.panel2,text="Locked", width=12,
                                  command=self.toggle_lock)
        self.lock_btn.grid(row=0,column=2)

        self.quit_button = tk.Button(self.panel2, text = "Quit",
                                 command = self.panel2.quit)
        self.quit_button.grid(row=0,column=3)

        
    def update(self):
        if (time.time() - self.now) > 1.0:
            self.wavelength.entry.update()
            self.now = time.time()
        exttrigger = self.lock_btn.config('text')[-1] == 'Unlocked'
        self.errsig = self.get_errsig(exttrigger=exttrigger)
        self.line.set_ydata(self.errsig)
        self.canvas.draw()
        self.after_id = self.root.after(self.sleepTime,self.update)
        
    def get_errsig(self,exttrigger=False):
        self.client.Call('errsig_measure',{'exttrigger':exttrigger})
        return self.client.Call('errsig_data')

    def get_wavelength(self):
        return self.client.Call('wm_read')

    def get_current(self):
        return self.client.Call('laser.read_current')

    def get_piezo(self):
        return self.client.Call('laser.read_piezo')

    def set_current(self,value):
        self.client.Call('laser.set_current',value)

    def set_piezo(self,value):
        self.client.Call('laser.set_piezo',value)
        self.current.entry.update()

    def do_nothing(self,*args):
        pass

    def get_ramp_amp(self):
        return self.client.Get('ramp_amp')

    def set_ramp_amp(self,value):
        self.client.Set('ramp_amp',value)
        self.client.Call('ramp_set')

    def toggle_lock(self):
        if self.lock_btn.config('text')[-1] == 'Unlocked':
            self.lock_btn.config(text='Locked')
            self.client.Call('lock_set',False)
            self.client.Call('ramp_set',True)
        else:
            self.lock_btn.config(text='Unlocked')
            self.client.Call('ramp_set',False)
            self.client.Call('lock_set',True)


root1 = tk.Tk()
w = window2(root1)
w.after_id = w.root.after(w.sleepTime,w.update)
w.root.mainloop()
