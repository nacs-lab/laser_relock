#!/usr/bin/python3

import zmq
from lock_control import lock_control
import functools
import inspect

class lock_control_server(object):
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
        self.lc = lock_control()
    def __del__(self):
        self.__sock.close()
        self.__ctx.destroy()
    def listen(self):
        timeout = 1 * 1000 # in milliseconds
        if self.__sock.poll(timeout) == 0:
            print('timeout')
            return 
        cmd = self.__sock.recv_string()
        args = self.__sock.recv_pyobj()
        try:
            attr = rgetattr(self.lc, cmd)
            attr_type = type(attr)
            print(attr_type)
            print('method? ',inspect.ismethod(attr))
            print(args)
            if inspect.ismethod(attr):
                if isinstance(args,tuple):
                    result = attr(*args)
                elif isinstance(args,dict):
                    result = attr(**args)
            else:
                result = attr
        except Exception as inst:
            print(inst)
            attr_type = None
        #self.__sock.send_string(str(attr_type))
        self.__sock.send_pyobj(result)

# from https://stackoverflow.com/questions/31174295/getattr-and-setattr...
# -on-nested-objects/31174427?noredirect=1#comment86638618_31174427

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

def main():
    # serv = lock_control_server('tcp://127.0.0.1:8000')
    serv = lock_control_server('tcp://192.168.0.110:9876')
    while True:
        try:
            serv.listen()
        except KeyboardInterrupt:
            break

if __name__=="__main__":
    main()
