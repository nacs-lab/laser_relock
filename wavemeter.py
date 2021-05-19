#!/usr/bin/python3

import csv
import pandas as pd

class wavemeter:
    def __init__(self,filename):
        self.filename = filename
        self.freq_lower = 0
        self.freq_upper = 1000000

    def read(self):
        with open(self.filename,'r',newline='') as f:
            # csv_reader = csv.reader(self.filename)
            last_line = f.readlines()[-1]
            print(last_line)
            
            
def main():
    import laser_settings as ls
    wm = wavemeter(ls.pump['wm_file'])
    wm.read()
            
if __name__=="__main__":
    main()
