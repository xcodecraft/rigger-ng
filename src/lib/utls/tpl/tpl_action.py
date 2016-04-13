#coding=utf8
import logging , re, os
import interface , utls.rg_io
_logger = logging.getLogger()


class conf:
    line_tag ='#%'
    var_tag  ='%'
    def __call__(self,name):
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
    """
DB : !T.chose
    prompt : "chose db!"
    options:
        - "mysql"
        - "orcal"
    """
    prompt  = ""
    # default = ""
    options = []
    def __call__(self,name):
        if hasattr(self,'prompt'):
            utls.rg_io.rgio.prompt(self.prompt)
        value = utls.rg_io.chose_item(self.options,name)
        return value


class input( interface.base,input_base):
    """
YOUNAME: !T.input
    prompt : "what's you name?"
    default : "boy"
    """
    default = None
    prompt  = None

    def __call__(self,name):
        prompt = self.get_prompt(name)
        value  = utls.rg_io.get_input_line(prompt,self.default_val())
        return value
    def __str__(self):
        return "%s , %s " %(self.default, self.prompt)

class bool(interface.base, input_base):
    """
    LOVE : !T.bool
        prompt : "love rg ?"
        default: "y"
    """
    default = None
    prompt  = None
    def __call__(self,name):
        prompt  = self.get_prompt(name)
        default = self.default_val()
        value   = utls.rg_io.get_input_line("%s [%s] ? (y/n)" %(prompt,name),default)
        if value is None :
            return value
        if value.lower()  == 'y' :
            return 'TRUE'
        if value.lower()  == 'n' :
            return 'FALSE'
        return None

