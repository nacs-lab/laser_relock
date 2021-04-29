#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anim

def plot_cont(fun,xmax):
    y = []
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    def update(i):
        yi = fun()
        y.append(yi)
        x = range(len(y))
        ax.clear()
        ax.plot(x,y)

    a = anim.FuncAnimation(fig, update, frames=xmax, repeat=False)
    plt.show()

def main():

    def func():
        x = np.random.randint(-10,10,1)
        return x[0]

    plot_cont(func,10)
    
if __name__ == '__main__':
    main()
