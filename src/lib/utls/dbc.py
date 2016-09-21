#coding=utf-8
import interface
import os
def not_none(val,errmsg) :
    if val is   None :
        raise interface.bug_exception( errmsg )
    return val

def must_true(val,errmsg) :
    if not val ==  True :
        raise interface.bug_exception( errmsg )
    return val
def must_exists( path) :
    if path is None or not os.path.exists(path) :
        raise interface.bug_exception("path not exists : %s" %path )

def must_file( path) :
    if path is None or not os.path.isfile(path) :
        raise interface.bug_exception("file not exists : %s" %path )

def must_obj(val,cls):
    if not isinstance(val,cls) :
        raise interface.bug_exception( " is not %s instance" %cls.__name__)
    return val

