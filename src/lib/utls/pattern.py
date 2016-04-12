class singleton(object):
    def __new__(cls, *args,** kwargs):
        if '_inst' not in vars(cls):
            cls._inst = super(singleton,cls).__new__(cls, * args, **kwargs)
        return  cls._inst


class end_keeper:
    def __init__(self,endcall) :
        self.endcall = endcall
    def cancel(self) :
        self.endcall = None
    def __enter__(self):
        pass
    def __exit__(self,*args,**kwargs):
        if self.endcall != None :
            self.endcall()

class fail_exception:
    def __init__(self,exception_obj) :
        self.exception_obj = exception_obj 
        pass
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None :
            raise self.exception_obj 
