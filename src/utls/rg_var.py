#coding=utf-8
import sys,re,os,string,logging
import setting
import utls.tpl
import interface
from utls.rg_io import *



def unound_promopt(key,tplstr):
    return "__NOFOUND_[%s]__" %key
def unound_break(key,tplstr):
    raise  interface.var_undefine("%s not define in [%s]" %(key,tplstr))

unfound_call= unound_break

class assginer :
    def __init__(self,tpl):
        self.tpl     = tpl
        self.unfound_call = unfound_call
    def assgin_value(self,match):
        var= str(match.group(1))
        var=var.upper()
        while True:
            try:
                val  = getattr(utls.tpl.var_obj(),var)
                rg_logger.info("[assgin] %-15s:%s" %(var,val ))
                return val
            except interface.var_undefine:
                rg_logger.error( "undefine %s, in %s" %(var,self.tpl))
                val = unfound_call(var,self.tpl)
                return val

def clean() :
    utls.tpl.var.clean()

def keep():
    utls.tpl.var.keep()
    pass
def rollback():
    utls.tpl.var.rollback()
    pass
def import_context(context) :
    utls.tpl.var.import_dict(context.__dict__)

def import_dict(d) :
    utls.tpl.var.import_dict(d)

def value_of(exp):
    tmp_exp = env_exp.var_proc(str(exp))
    return env_exp.fun_proc(tmp_exp)

class env_exp:

    @staticmethod
    def funval_of_match (match):
        fun = "inner." + str(match.group(0))
        res = eval(fun)
        return str(res)

    @staticmethod
    def var_proc(string):
        tpl     = string.strip()
        var_exp = re.compile(r'\$\{(\w+)\}')
        ass     = assginer(tpl)
        # rg_logger.debug("env_exp.var_proc : %s" %tpl  )
        while var_exp.search(tpl):
            # rg_logger.debug("env.var(%s)" %tpl)
            tpl = var_exp.sub(ass.assgin_value,tpl)
        return tpl

    @staticmethod
    def fun_proc(string):
        exp = re.compile(r'(_\w+_\(.*\))')
        try:
            new = exp.sub(env_exp.funval_of_match,str(string))
            return new
        except:
            print("fun:" + string) ;
            raise

    @staticmethod
    def value(exp):
        tmp_exp = env_exp.var_proc(str(exp))
        return env_exp.fun_proc(tmp_exp)
