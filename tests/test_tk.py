import tkinter as tk

class window2:
    def __init__(self, master1):
        self.panel2 = tk.Frame(master1)
        self.panel2.grid()
        
        self.button2 = tk.Button(self.panel2, text = "Quit",
                                 command = self.panel2.quit)
        self.button2.grid()
        
        self.button3 = tk.Button(self.panel2, text = "get info",
                                 command = self.get_info)
        self.button3.grid()
        
        vcmd = (master1.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.text1 = tk.Entry(self.panel2,
                              validate = 'key',validatecommand = vcmd)
        self.text1.grid()
        self.text1.bind('<Up>', self.arrowKey)
        self.text1.bind('<Down>', self.arrowKey)
        self.text1.focus()
        self.value = 1000.0
        self.text1.insert(0,self.value)
        
    def arrowKey(self,event):
        digits = len(self.text1.get())
        dec_pos = self.text1.get().find('.')
        curs_pos = self.text1.index(tk.INSERT)
        if dec_pos < 0:
            self.value = self.value + ((1 if event.keysym=='Up' else -1)*
                                       (10.0**(digits-curs_pos)))
        else:
            self.value = self.value
            if curs_pos > dec_pos:                
                self.value = self.value + ((1 if event.keysym=='Up' else -1)*
                                           (10.0**(dec_pos-curs_pos+1)))
            else:
                self.value = self.value + ((1 if event.keysym=='Up' else -1)*
                                           (10.0**(dec_pos-curs_pos)))
        self.text1.delete(0,tk.END)
        self.text1.insert(0,self.value)
        self.text1.icursor(curs_pos)
    def get_info(self):
        print(self.text1.index(tk.INSERT))

    def validate(self, action, index, value_if_allowed,prior_value,
                 text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False 
        else:
            return True

root1 = tk.Tk()
window2(root1)
root1.mainloop()
