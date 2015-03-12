#coding=utf-8
import interface
def not_none(val,errmsg) :
    if val is   None :
        raise interface.rigger_exception( errmsg )
    return val

def must_true(val,errmsg) :
    if not val ==  True :
        raise interface.rigger_exception( errmsg )
    return val
