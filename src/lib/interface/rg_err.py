#coding=utf-8
class rigger_exception(Exception):
    pass

class bug_exception(Exception) :
    pass

class user_break(rigger_exception):
    pass

class badargs_exception(rigger_exception):
    pass

class cmd_use_error(rigger_exception):
    def __init__(self,cmd,message):
        self.cmd = cmd 
        rigger_exception.__init__(self,message)

class res_use_error(rigger_exception):
    def __init__(self,res,message):
        self.res = res
        rigger_exception.__init__(self,message)

class depend_exception(rigger_exception) :
    def __init__(self,monitor):
        self.monitor = monitor
    pass

class var_undefine(rigger_exception):
    pass
