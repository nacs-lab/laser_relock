import tkinter as tk
from NumericEntry import *

class window2:
    def __init__(self, master1):
        self.panel2 = tk.Frame(master1)
        self.panel2.grid()
        
        self.button2 = tk.Button(self.panel2, text = "Quit",
                                 command = self.panel2.quit)
        self.button2.grid()
        
        self.num1 = NumericEntry(master1,self.panel2,1000.0)
        self.num1.grid()

        self.num2 = NumericEntry(master1,self.panel2,1000.0)
        self.num2.grid()


root1 = tk.Tk()
window2(root1)
root1.mainloop()
