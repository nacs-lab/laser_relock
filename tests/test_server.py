#!/usr/bin/python3

import zmq

class test_server(object):
    def recreate_sock(self):
        if self.__sock is not None:
            self.__sock.close()
        
    def __init__(self,url):
        self.__url = url
        self.__ctx = zmq.Context()
        self.__sock = None
        self.recreate_sock()
