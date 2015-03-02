#coding=utf8
import re
import interface , utls.rg_var , rg_model



class system (interface.control_box,interface.base):
    def _before(self,context):
        utls.rg_var.keep()
        context.keep()
        pass
    def _after(self,context):
        context.rollback()
        utls.rg_var.rollback()
        pass
    def _resname(self):
        return self.name
    def _info(self):
        return ""

class project(interface.control_box, interface.base) :
    def _resname(self):
        tag = self.__class__.__name__
        return tag
    def _info(self):
        return ""
    pass

class xmodule(interface.control_box,interface.base) :
    def _resname(self):
        tag = self.__class__.__name__
        return tag


class env(interface.resource):
    def _resname(self):
        if hasattr(self,'name'):
            return  "%s(%s)" %(self._clsname(),self.name)
        return self._clsname()



