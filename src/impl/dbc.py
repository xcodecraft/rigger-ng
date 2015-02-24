#coding=utf-8
def not_none(fun) :
    exec_value = fun()
    if exec_value ==  None :
        raise rigger_exception( fun.err_msg) 
    return exec_value 

def must_true(fun) :
    exec_value = fun()
    if not exec_value :
        raise rigger_exception( fun.err_msg) 
    return exec_value 
