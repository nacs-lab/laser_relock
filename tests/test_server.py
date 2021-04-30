#!/usr/bin/python3

import zmq
import array
import time

class test_server(object):
    def recreate_sock(self):
        if self.__sock is not None:
            self.__sock.close()
        self.__sock = self.__ctx.socket(zmq.REP) # Reply socket
        self.__sock.setsockopt(zmq.LINGER, 0) # discards messages when socket is closed
        self.__sock.bind(self.__url)
    def __init__(self, url):
        self.__url = url
        self.__ctx = zmq.Context()
        self.__sock = None
        self.recreate_sock()
    def __del__(self):
        self.__sock.close()
        self.__ctx.destroy()
    def recv_int(self):
        timeout = 1 * 1000 # in milliseconds
        if self.__sock.poll(timeout) == 0:
            return
        return int.from_bytes(self.__sock.recv(), byteorder = 'little')
    def send_int(self,val):
        return self.__sock.send(int(val).to_bytes(4, byteorder = 'little'))

serv = test_server('tcp://127.0.0.1:8000')

while True:
    val = serv.recv_int()

    if val==None:
        print('timeout')
        continue
    
    print(val)
    time.sleep(0.5)
    serv.send_int(val+1)
