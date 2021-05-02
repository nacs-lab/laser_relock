#!/usr/bin/python

'''
hello world for zmq between raspi and pc outside lab
server part
'''


import zmq
import array
import time 

class test_client(object):
    def recreate_sock(self):
        if self.__sock is not None:
            self.__sock.close()
        self.__sock = self.__ctx.socket(zmq.REQ) # Request socket
        self.__sock.setsockopt(zmq.LINGER, 0) # discards messages when socket is closed
        self.__sock.connect(self.__url)
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
    def send_int(self, value):
        return self.__sock.send(value.to_bytes(4, byteorder='little'))
    def send_cmd(self, value):
        self.__sock.send_string(value)
    def recv_data(self):
        timeout = 1 * 1000 # in milliseconds
        if self.__sock.poll(timeout) == 0:
            return
        
        int.from_bytes(self.__sock.recv(), byteorder = 'little')


# cl = test_client('tcp://127.0.0.1:8000')
cl = test_client('tcp://nacs.nigrp.org:5633')

val = 0

while True:
    cl.send_int(val)   
    time.sleep(0.5)
    val = cl.recv_int()
    print(val)
