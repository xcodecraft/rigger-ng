#coding=utf8
import re,logging
import interface , utls.rg_var , rg_model
from utls.rg_io import rgio,run_struct


_logger = logging.getLogger()

class system (interface.control_box,interface.base):
    """
__sys:
    -  !R.system
        name: "test"
        res:
            - !R.vars
                    TEST_CASE: "${HOME}/devspace/rigger-ng/test/main.py"
            - !R.echo
                value : "${TEST_CASE}"
    """
    def _before(self,context):

        _logger.info("system:%s start" %(self.name))
        utls.rg_var.keep()
        context.keep()

    def _after(self,context):
        context.rollback()
        utls.rg_var.rollback()
        _logger.info("system:%s end" %(self.name))

    def _resname(self):
        return self.name
    def _info(self,context):
        rgio.struct_out("system: %s" %(self.name))
        interface.control_box._info(self,context)

class project(interface.control_box, interface.base) :
    """

    """
    def _resname(self):
        tag = self.__class__.__name__
        return tag
    def _info(self,context):
        rgio.struct_out("project: %s" %(self.name))
        interface.control_box._info(self,context)


class prj_main(interface.control_box, interface.base) :
    """
    """
    name = "main"
    def _info(self,context):
        rgio.struct_out("rg: %s" %(self.name))
        interface.control_box._info(self,context)

class xmodule(interface.control_box,interface.base) :
    """

    """
    def _resname(self):
        tag = self.__class__.__name__
        return tag
    def _info(self,context):
        rgio.struct_out("xmodule: %s" %(self.name))
        interface.control_box._info(self,context)


class env(interface.resource):
    """

    """
    def _resname(self):
        if hasattr(self,'name'):
            return  "%s(%s)" %(self._clsname(),self.name)
        return self._clsname()
    def _info(self,context):
        rgio.struct_out("env: %s" %(self.name))



