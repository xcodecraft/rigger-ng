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

def must_obj(val,cls):
    if not isinstance(val,cls) :
        raise interface.rigger_exception( " is not %s instance" %cls.__name__)
    return val
