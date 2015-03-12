#coding=utf8
import logging , re, os
import interface , utls.rg_io
_logger = logging.getLogger()


class conf:
    line_tag ='#%'
    var_tag  ='%'
    def execute(self,name):
        pass

class input_base:
    def get_prompt(self,name) :
        prompt = "please input [%s] value:" %name
        if self.prompt is not None :
            prompt = self.prompt
        return prompt

    def default_val(self) :
        default = None
        if  self.default is not None :
            default = self.default
        return default

class chose(interface.base):
    def execute(self,name):
        if hasattr(self,'prompt'):
            rgio.prompt(self.prompt)
        value = chose_item(self.options,name)
        return value

class path_chose(interface.base):
    root   = ""
    prompt = None

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

class input( interface.base,input_base):
    default = None
    prompt  = None

    def execute(self,name):
        prompt = self.get_prompt(name)
        value  = utls.rg_io.get_input_line(prompt,self.default_val())
        return value
    def __str__(self):
        return "%s , %s " %(self.default, self.prompt)

class bool(interface.base, input_base):
    default = None
    prompt  = None
    def execute(self,name):
        prompt = self.get_prompt(name)
        default = self.get_default()
        value = get_input_line("%s [%s] ? (y/n)" %(prompt,name),default)
        if value is None :
            return value
        if value.lower()  == 'y' :
            return 'TRUE'
        if value.lower()  == 'n' :
            return 'FALSE'
        return None

