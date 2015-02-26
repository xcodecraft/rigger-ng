#coding=utf8
# import  validate,utls , conf_base
# from dev import *
import logging , re, os
import interface
_logger = logging.getLogger()
class conf:
    line_tag ='#%'
    var_tag  ='%'
    def execute(self,name):
        pass
    pass

class chose(interface.base):
    def execute(self,name):
        if hasattr(self,'prompt'):
            rgio.prompt(self.prompt)
        value = chose_item(self.options,name)
        return value
class path_chose(interface.base):
    _root   = ""
    _prompt = None

    def proc_files(self,arg,dirname,names):
        if dirname == self.root :
            self.options = names
    def execute(self,name):
        self.root = utls.env_exp.value(self.root)
        validate.v_path(self.root)
        os.path.walk(self.root,self.proc_files,None)
        if  self.prompt is not None:
            rgio.prompt(self.prompt)
        value = chose_item(self.options,name)
        return value

class input( interface.base):
    _default = None
    _prompt  = None
    def execute(self,name):
        default = None
        if  self.default is not None :
            default = self.default
        prompt = "please input [%s] value:" %name
        if self.prompt is not None :
            prompt = self.prompt  + "[%s]" %name
        value = get_input_line(prompt,default)
        return value

class bool(interface.base):
    _default = None
    _prompt  = None
    def execute(self,name):
        prompt = name
        if self.prompt is not None :
            prompt = self.prompt
        default = None
        if  self.default is not None :
            default = self.default
        value = get_input_line("%s [%s] ? (y/n)" %(prompt,name),default)
        if value is None :
            return value
        if value.lower()  == 'y' :
            return 'TRUE'
#            return str_bool(True)
        if value.lower()  == 'n' :
            return 'FALSE'
#            return str_bool(False)
        return None

