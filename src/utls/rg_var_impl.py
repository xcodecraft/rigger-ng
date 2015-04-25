#coding=utf-8
import sys,re,os,string,logging
import setting
import interface
from utls.rg_io import *
from tpl.tpl_var import *

def unound_promopt(key,tplstr):
    return "__NOFOUND_[%s]__" %key
def unound_break(key,tplstr):
    raise  interface.var_undefine("%s not define in [%s]" %(key,tplstr))

unfound_call= unound_break

class assginer :
    def __init__(self,tpl,rgvar_gods):
        self.tpl          = tpl
        self.rgvar_gods     = rgvar_gods
        self.unfound_call = unfound_call
    def assgin_value(self,match):
        var= str(match.group(1))
        var=var.upper()
        while True:
            try:
                val  = getattr(self.rgvar_gods,var)
                rg_logger.info("[assgin] %-15s:%s" %(var,val ))
                return val
            except interface.var_undefine:
                rg_logger.error( "undefine %s, in %s" %(var,self.tpl))
                val = unfound_call(var,self.tpl)
                return val


class rgvar_god(utls.pattern.singleton):
    def __init__(self):
        # self.impl     = combo_porp(dict_porp(os.environ),empty_porp())
        self.impl     = combo_porp(safe_env_porp.ins(),empty_porp())
        self.restores = []

    def import_dict(self,dict_obj):
        utls.dbc.must_true(isinstance(dict_obj,dict)," rgvar_god.import_dict need dict obj" )
        dict_obj  = upper_dict(dict_obj)
        self.impl = combo_porp(dict_porp(dict_obj),self.impl)

    def import_porp(self,porpobj) :
        self.impl = combo_porp(porpobj,self.impl)

    def import_attr(self,porpobj) :
        self.impl = combo_porp(porp_proxy(porpobj),self.impl)

    def import_str(self,asstr):
        dict_obj  = parse_assgin(asstr)
        self.impl = combo_porp(dict_porp(dict_obj),self.impl)

    def export_env(self) :
        self.impl.export(os.environ)
    def export2dict(self,target) :
        self.impl.export(target)

    def current(self):
        return self.impl

    def clean(self):
        self.__init__()
    def keep(self) :
        self.restores.append( copy.copy(self.impl))
    def rollback(self) :
        self.impl = self.restores.pop()



class env_exp:

    @staticmethod
    def funval_of_match (match):
        fun = "inner." + str(match.group(0))
        res = eval(fun)
        return str(res)

    @staticmethod
    def var_proc(string,tplvars):
        # tpl     = string.strip()
        tpl     = string
        var_exp = re.compile(r'\$\{(\w+)\}')
        ass     = assginer(tpl,tplvars)
        while var_exp.search(tpl):
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

    # @staticmethod
    # def value(exp):
    #     tmp_exp = env_exp.var_proc(str(exp))
    #     return env_exp.fun_proc(tmp_exp)
