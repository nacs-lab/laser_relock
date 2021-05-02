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
    def Call(self,name,*args):
        self.__sock.send_string("call",zmq.SNDMORE)
        self.__sock.send_string(name,zmq.SNDMORE)
        if len(args)==1 and isinstance(args[0],dict):
            self.__sock.send_pyobj(args[0])
        else:
            self.__sock.send_pyobj(args)
        return self.__sock.recv_pyobj()
    def Get(self,name):
        self.__sock.send_string("get",zmq.SNDMORE)
        self.__sock.send_string(name)
        return self.__sock.recv_pyobj()
    def Set(self,name,value):
        self.__sock.send_string("set",zmq.SNDMORE)
        self.__sock.send_string(name,zmq.SNDMORE)
        self.__sock.send_pyobj(value)
        return self.__sock.recv_pyobj()


def main():
    # cl = lock_control_client('tcp://127.0.0.1:8000')
    cl = lock_control_client('tcp://nacs.nigrp.org:5633')
    result = cl.Get('wm.filename')
    print(result)

    result = cl.Call('errsig.measure',{'continuous':True})
    print(result)

    result = cl.Call('errsig.get_status')
    print(result)

    result = cl.Call('errsig.get_index')
    print(result)

    result = cl.Call('errsig.stop')
    print(result)

    result = cl.Call('errsig.get_status')
    print(result)

    result = cl.Call('errsig.data')
    print(result)

if __name__=="__main__":
    main()