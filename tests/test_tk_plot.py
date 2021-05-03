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
        self.sleepTime = 300

        self.current_dummy = self.get_current()
        self.piezo_dummy = self.get_piezo()
        self.wavelength_dummy = self.get_wavelength()

        # upper frame with numbers & buttons
        self.panel1 = tk.Frame(self.root)
        self.panel1.grid()

        # buttons
        self.quit_button = tk.Button(self.panel1, text = "Quit",
                                 command = self.panel1.quit)
        self.quit_button.grid(column=3)

        # initialize plot
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.line, = self.ax1.plot(self.get_errsig())
        self.canvas = FigureCanvasTkAgg(self.fig,master=self.root)
        self.canvas.get_tk_widget().grid()
        self.canvas.mpl_connect('close_event', self.on_close)

        # lower frame with numbers & buttons
        self.panel2 = tk.Frame(self.root)
        self.panel2.grid()
        
        
        # numeric entries
        self.current = NumericEntry(self.root,self.panel2,self.get_current_dummy,self.set_current_dummy)
        self.current.grid(row=0,column=0)

        self.piezo = NumericEntry(self.root,self.panel2,self.get_piezo_dummy,self.set_piezo_dummy)
        self.piezo.grid(row=1,column=0)

        self.wavelength = NumericEntry(self.root,self.panel2,self.get_wavelength,self.do_nothing)
        self.wavelength.grid(row=1,column=0)

    def update_plot(self):
        self.errsig = self.get_errsig()
        self.line.set_ydata(self.errsig)
        self.canvas.draw()
        self.after_id = self.root.after(self.sleepTime,self.update_plot)
        
    def on_close(self,ind):
        self.root.after_cancel(self.after_id)
        sys.exit()
        
    def get_errsig(self):
        self.client.Call('errsig.measure')
        return self.client.Call('errsig.data')

    def get_wavelength(self):
        return self.client.Call('wm.read')

    def get_current(self):
        return self.client.Call('laser.read_current')

    def get_piezo(self):
        return self.client.Call('laser.read_piezo')

    def get_current_dummy(self):
        return self.current_dummy

    def get_piezo_dummy(self):
        return self.piezo_dummy

    def set_current_dummy(self,value):
        self.current_dummy = value

    def set_piezo_dummy(self,value):
        self.piezo_dummy = value

    def do_nothing(self,*args):
        pass


root1 = tk.Tk()
w = window2(root1)
w.after_id = w.root.after(w.sleepTime,w.update_plot)
w.root.mainloop()
