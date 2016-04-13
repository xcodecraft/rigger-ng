#coding=utf-8
import interface
import os

def not_none(val,errmsg) :
    if val is None :
        raise interface.rigger_exception( errmsg )
    return val

def must_true(val,errmsg) :
    if not val ==  True :
        raise interface.rigger_exception( errmsg )
    return val

def ok(val,errmsg) :
    if not val :
        raise interface.rigger_exception( errmsg )
    return val
def must_exists( path) :
    if path is None or not os.path.exists(path) :
        raise interface.rigger_exception("file not exists : %s" %path )

