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
        
        # buttons
        self.button2 = tk.Button(self.panel2, text = "Quit",
                                 command = self.panel2.quit)
        self.button2.grid()
        
        # numeric entries
        self.current = NumericEntry(self.root,self.panel2,1000.0)
        self.current.grid()

        self.piezo = NumericEntry(self.root,self.panel2,1000.0)
        self.piezo.grid()

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

    def get_current(self):
        return self.client.Call('laser.read_current')

    def get_piezo(self):
        return self.client.Call('laser.read_piezo')


root1 = tk.Tk()
w = window2(root1)
w.after_id = w.root.after(w.sleepTime,w.update_plot)
w.root.mainloop()
