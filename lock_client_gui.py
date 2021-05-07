#!/usr/bin/python3

import tkinter as tk
from NumericEntry import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np 
import sys
from lock_control_client import lock_control_client
import time

class window2:
    def __init__(self, master1):
        
        self.client = lock_control_client()
        self.root = master1
        self.sleepTime = 10
        self.now = time.time()

        # initialize plot
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.line, = self.ax1.plot(self.get_errsig())
        self.canvas = FigureCanvasTkAgg(self.fig,master=self.root)
        self.canvas.get_tk_widget().grid()
        self.canvas.mpl_connect('close_event', self.on_close)
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
                                              self.get_wavelength,self.do_nothing,label="Freq")
        self.wavelength.grid(row=0,column=1)

        self.ramp_amp = NumericEntryLabeled(self.root,self.panel2,self.get_ramp_amp,
                                     self.set_ramp_amp,label="RampAmp")
        self.ramp_amp.grid(row=1,column=1)

        # lock, ramp, quit buttons
        self.ramp_btn = tk.Button(self.panel2,text="Ramp On", width=12, command=self.toggle_ramp)
        self.ramp_btn.grid(row=0,column=2)

        self.lock_btn = tk.Button(self.panel2,text="Lock", width=12, command=self.toggle_lock)
        self.lock_btn.grid(row=1,column=2)

        self.quit_button = tk.Button(self.panel2, text = "Quit",
                                 command = self.panel2.quit)
        self.quit_button.grid(row=0,column=3)

        
    def update(self):
        if (time.time() - self.now) > 3.0:
            #print('update wl')
            self.wavelength.update()
            self.now = time.time()
        exttrigger = self.ramp_btn.config('text')[-1] == 'Ramp On'
        self.errsig = self.get_errsig(exttrigger=exttrigger)
        self.line.set_ydata(self.errsig)
        self.canvas.draw()
        self.after_id = self.root.after(self.sleepTime,self.update)
        
    def on_close(self,ind):
        self.root.after_cancel(self.after_id)
        sys.exit()
        
    def get_errsig(self,exttrigger=True):
        self.client.Call('errsig.measure',{'exttrigger':exttrigger})
        return self.client.Call('errsig.data')

    def get_wavelength(self):
        #print('get wavelength')
        return self.client.Call('wm.read')

    def get_current(self):
        #print('get current')
        return self.client.Call('laser.read_current')

    def get_piezo(self):
        #print('get pzt')
        return self.client.Call('laser.read_piezo')

    def set_current(self,value):
        #print('set current')
        self.client.Call('laser.set_current',value)

    def set_piezo(self,value):
        #print('set pst')
        self.client.Call('laser.set_piezo',value)

    def do_nothing(self,*args):
        pass

    def toggle_ramp(self):
        if self.ramp_btn.config('text')[-1] == 'Ramp On':
            self.ramp_btn.config(text='Ramp Off')
            self.client.Call('ramp.set',False)
        else:
            self.ramp_btn.config(text='Ramp On')
            self.client.Call('ramp.set',True)

    def get_ramp_amp(self):
        #print('get ramp amp')
        return self.client.Get('ramp.amp')

    def set_ramp_amp(self,value):
        #print('set ramp amp')
        self.client.Set('ramp.amp',value)
        self.client.Call('ramp.set')

    def toggle_lock(self):
        if self.lock_btn.config('text')[-1] == 'Lock':
            self.lock_btn.config(text='Unlock')
            self.client.Call('lock.set',False)
        else:
            self.lock_btn.config(text='Lock')
            self.client.Call('lock.set',True)

root1 = tk.Tk()
w = window2(root1)
w.after_id = w.root.after(w.sleepTime,w.update)
w.root.mainloop()
