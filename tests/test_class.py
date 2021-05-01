#!/usr/bin/python3

class parent_class:
    def __init__(self):
        self.x = 0
        self.child = self._child_class()

    class _child_class:
        def __init__(self):
            self.y = 0

        def child_func(self,arg=0):
            self.y = arg
            return self.y
        
        class __metaclass__(type):
            def __get__(self,instance,owner):
                self.owner = owner
                return self
        

#obj = parent_class()
# print(obj.child.child_func())
