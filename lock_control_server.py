#!/usr/bin/python3

import zmq
from lock_control import lock_control
import functools

# URL = 'tcp://127.0.0.1:8000'
URL = 'tcp://192.168.0.105:9876'

class lock_control_server(object):
    def recreate_sock(self):
        if self.__sock is not None:
            self.__sock.close()
        self.__sock = self.__ctx.socket(zmq.REP) # Reply socket
        self.__sock.setsockopt(zmq.LINGER, 0) # discards messages when socket is closed
        self.__sock.bind(self.__url)

    def __init__(self,url=URL):
        self.__url = url
        self.__ctx = zmq.Context()
        self.__sock = None
        self.recreate_sock()
        self.lc = dict()
        self.lc['pump'] = lock_control('pump')
        self.lc['stokes'] = lock_control('stokes')

    def __del__(self):
        self.__sock.close()
        self.__ctx.destroy()
        print('closed connection')

    def listen(self):
        timeout = 1 * 1000 # in milliseconds
        if self.__sock.poll(timeout) == 0:
            return
        cmd = self.__sock.recv_string()
        name = self.__sock.recv_string()
        laser = self.__sock.recv_string()
        if cmd=="get":
            result = self.Get(laser,name)
        elif cmd=="set":
            value = self.__sock.recv_pyobj()
            result = self.Set(laser,name,value)
        elif cmd=="call":
            args = self.__sock.recv_pyobj()    
            result = self.Call(laser,name,args)
        else:
            result = Exception('Command must be one of ("get","set","call")')
        try:
            self.__sock.send_pyobj(result)
        except:
            self.__sock.send_string('incompatible type')

    def Get(self,laser,name):
        try:
            result = rgetattr(self.lc[laser], name)
        except Exception as inst:
            print(inst)
            result = str(inst)
        return result

    def Set(self,laser,name,value):
        try:
            result = rsetattr(self.lc[laser], name, value)
        except Exception as inst:
            print(inst)
            result = str(inst)
        return result

    def Call(self,laser,name,args):
        try:
            attr = rgetattr(self.lc[laser], name)
            if isinstance(args,tuple):
                result = attr(*args)
            elif isinstance(args,dict):
                result = attr(**args)
        except Exception as inst:
            print(inst)
            result = str(inst)
        return result

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
    serv = lock_control_server()
    while True:
        try:
            serv.listen()
        except KeyboardInterrupt:
            break

if __name__=="__main__":
    main()
