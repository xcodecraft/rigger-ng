#coding=utf-8
class rigger_exception(Exception):
    pass

class user_break(rigger_exception):
    pass

class badargs_exception(rigger_exception):
    pass

class depend_exception(rigger_exception) :
    def __init__(self,monitor):
        self.monitor = monitor
    pass

class var_undefine(rigger_exception):
    pass
