#!/usr/bin/python

import zmq
import types

URL = 'tcp://nacs.nigrp.org:5633'

class lock_control_client(object):
    def recreate_sock(self):
        if self.__sock is not None:
            self.__sock.close()
        self.__sock = self.__ctx.socket(zmq.REQ) # Request socket
        self.__sock.setsockopt(zmq.LINGER, 0) # discards messages when socket is closed
        self.__sock.connect(self.__url)
    def __init__(self, url=URL):
        self.__url = url
        self.__ctx = zmq.Context()
        self.__sock = None
        self.recreate_sock()
    def __del__(self):
        self.__sock.close()
        self.__ctx.destroy()
    def get(self,value,args=None):
        self.__sock.send_string(value,zmq.SNDMORE)
        self.__sock.send_pyobj(args)
        val_type = self.__sock.recv_string()
        print(val_type)


def main():
    # cl = lock_control_client('tcp://127.0.0.1:8000')
    cl = lock_control_client('tcp://nacs.nigrp.org:5633')
    val = 'laser.set_current'
    cl.get(val)

if __name__=="__main__":
    main()