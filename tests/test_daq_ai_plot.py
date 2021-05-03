#!/usr/bin/python3

from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
from mcc_daq import mcc_daq

def main():
    daq = mcc_daq(0)
    daq.connect()
    daq.ai.set_params(channels=[0],rate=48000,samples=1000,triggers=1)
    daq.ai.measure(continuous=False)
    
    root = Tk()
    root.geometry('640x500')

    sleepTime = 100

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    line, = ax1.plot(daq.ai.data)

    after_id = ''

    def update_plot():
        daq.ai.measure()
        line.set_ydata(daq.ai.data)
        canvas.draw()
        after_id = root.after(sleepTime,update_plot)

    def on_close(ind):
        root.after_cancel(after_id)
        sys.exit()

    def stop_fun():
        root.after_cancel(after_id)
        root.destroy()

    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.get_tk_widget().pack()
    canvas.mpl_connect('close_event', on_close)
    
    frame = Frame(root)
    frame.pack()
    stopbutton = Button(master=root,text="Stop",command=stop_fun)
    stopbutton.pack(side = BOTTOM)

    after_id = root.after(sleepTime,update_plot)
    root.mainloop()

if __name__=="__main__":
    main()
