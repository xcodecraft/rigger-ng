#coding=utf8
import re,logging
import interface,utls.rg_var
import modules
import utls.dbc
# from utls.dbc import *
from utls.rg_io import  rgio , run_struct,rg_logger

class vars(interface.resource):
    """
    !R.vars:
        A: 1
        B: "hello"
    """

    name = "vars"
    def depend_check(self,context) :
        pass

    def _allow(self,context):
        return True
    def _before(self,context):
        # import pdb
        # pdb.set_trace()
        items = self.__dict__
        # run_struct.push("res.var")

        for name , val in   items.items():
            if re.match(r'__.+__',name):
                continue
            name= name.upper()
            setattr(context,name,val)
        utls.rg_var.import_dict(items)

    def _after(self,context):
        pass


    def _info(self,context):
        items = self.__dict__
        rgio.struct_out("vars:")
        for name , val in   items.items():
            if re.match(r'__.+__',name):
                continue
            name= name.upper()
            rgio.struct_out("%s = %s" %(name,val),1)

class echo(interface.resource) :
    """
        !R.echo :
            value : "${PRJ_ROOT}"
    """
    name = "echo"
    def _allow(self,context):
        return True
    def _before(self,context):
        pass
    def _config(self,context):
        v = utls.rg_var.value_of(self.value)
        print("[echo] %s :%s " %(self.value,v))

class assert_eq(interface.resource) :
    """
    !R.assert
        value  : "${APP_SYS}"
        expect : "test"
    """
    name = "assert_eq"
    def _allow(self,context):
        return True
    def _config(self,context):
        self.assert_eq(context)
    def assert_eq(self,context):
        value  = utls.rg_var.value_of(self.value)
        expect = utls.rg_var.value_of(self.expect)
        if value != expect :
            raise interface.rigger_exception("value: %s , expect : %s " %(value,expect))
    def _start(self,context) :
        self.assert_eq(context)


class system (interface.control_box,interface.base):
    """
__sys:
    -  !R.system
        _name: "test"
        _res:
            - !R.vars
                    TEST_CASE: "${HOME}/devspace/rigger-ng/test/main.py"
            - !R.echo
                value : "${TEST_CASE}"
    """
    def _before(self,context):
        rg_logger.info("system:%s start" %(self._name))
        utls.rg_var.keep()
        context.keep()

    def _after(self,context):
        context.rollback()
        utls.rg_var.rollback()
        rg_logger.info("system:%s end" %(self._name))

    def _resname(self):
        return self._name

    def _check(self,context):
        self._check_print(True,"system: %s" %self._name)
        interface.control_box._check(self,context)

    def _info(self,context):
        rgio.struct_out("system: %s" %(self._name))
        interface.control_box._info(self,context)

class project(interface.control_box, interface.base) :
    """

    """
    def _resname(self):
        tag = self.__class__.__name__
        return tag
    def _info(self,context):
        rgio.struct_out("project: %s" %(self._name))
        interface.control_box._info(self,context)

    def _check(self,context):
        self._check_print(True,"project: %s" %self._name)
        interface.control_box._check(self,context)

    def _before(self,context):
        rg_logger.info("project: start")

    def _after(self,context):
        rg_logger.info("project: end")

class prj_main(interface.control_box, interface.base) :
    """
    """
    _name = "main"
    def _info(self,context):
        rgio.struct_out("rg: %s" %(self._name))
        interface.control_box._info(self,context)
    def _before(self,context):
        rg_logger.info("main: start")

    def _after(self,context):
        rg_logger.info("main: end")

class modul(interface.control_box,interface.base) :
    """
    !R.modul
        _name : "php-web"
        _res  :
            ...
    """
    _name = ""
    def _resname(self):
        tag = self.__class__.__name__
        return tag
    def _info(self,context):
        rgio.struct_out("modul : %s" %(self._name))
        interface.control_box._info(self,context)

    def _before(self,context):
        # run_struct.push("modul %s" %(self._name))
        rg_logger.info("modul:%s start" %(self._name))
        utls.rg_var.keep()
        context.keep()

    def _after(self,context):
        context.rollback()
        utls.rg_var.rollback()
        rg_logger.info("modul:%s end" %(self._name))
        # run_struct.pop()

class using(interface.resource):
    """
    !R.using
      path  : "/usr/local/lib/rigger-ng/php.yaml"
      modul : "php-web"
    """
    path  = ""
    modul = ""
    def _allow(self,context):
        return True
    def _before(self,context):
        # run_struct.push("using.module.%s" %self.modul)
        self.path       = utls.rg_var.value_of(self.path)
        if len(self.path) > 0 :
            modules.load(self.path)
        key            = utls.rg_var.value_of(self.modul)
        msg = "load modul %s from '%s' failed! " %(key,self.path)
        self.modul_obj = utls.dbc.not_none(modules.find(key), msg)
        self.modul_obj._before(context)

    def _after(self,context):
        self.modul_obj._after(context)
        # run_struct.pop()

    def _start(self,context):
        self.modul_obj._start(context)

    def _stop(self,context):
        self.modul_obj._stop(context)

    def _reload(self,context):
        self.modul_obj._reload(context)

    def _config(self,context):
        self.modul_obj._config(context)

    def _data(self,context):
        self.modul_obj._data(context)

    def _check(self,context):
        self.modul_obj._check(context)

    def _clean(self,context):
        self.modul_obj._clean(context)

    def _info(self,context):
        self.modul_obj._info(context)

class env(vars):
    """

    """
    def _resname(self):
        return  "%s(%s)" %(self.__class__.__name__,self._name)
    def _info(self,context):
        rgio.struct_out("env: %s" %(self._name))

    def _before(self,context):
        rg_logger.info("env:%s start" %(self._name))
        vars._before(self,context)

    def _after(self,context):
        rg_logger.info("env:%s end" %(self._name))
