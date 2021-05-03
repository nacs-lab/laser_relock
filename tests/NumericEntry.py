#!/usr/bin/python3

import tkinter as tk

class NumericEntry(tk.Entry):
    def __init__(self,root,panel,value=0.0):
        vcmd = (root.register(self.validate),'%d','%i','%P','%s','%S','%v','%V','%W')
        tk.Entry.__init__(self,panel,validate='key',validatecommand=vcmd)
        self.bind('<Up>', self.arrowKey)
        self.bind('<Down>', self.arrowKey)
        self.value = value
        self.insert(0,f'{self.value:.2f}')
        
    def validate(self, action, index, value_if_allowed,prior_value,
                 text, validation_type, trigger_type, widget_name):
        if (' ' in value_if_allowed):
            return False
        elif value_if_allowed:
            try:
                self.value = float(value_if_allowed)
                return True
            except ValueError:
                return False 
        else:
            return True

    def arrowKey(self,event):
        digits = len(self.get())
        dec_pos = self.get().find('.')
        curs_pos = self.index(tk.INSERT)
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
        new_digits = len(f'{self.value:.2f}')
        self.delete(0,tk.END)
        self.insert(0,f'{self.value:.2f}')
        self.icursor(curs_pos + new_digits - digits)