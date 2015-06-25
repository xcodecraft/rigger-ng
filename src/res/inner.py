#coding=utf8
import re,logging
import interface,utls.rg_var
import node
import utls.dbc , utls.check
import res.node
import copy
# from utls.dbc import *
from utls.rg_io import  rgio , run_struct,rg_logger
from base import *
from utls.tpl.tpl_var import safe_env_porp

import  res.files

class project(interface.resource,res_utls) :
    """
    """
    root = ""
    name = ""
    env  = 'HOME,USER,PRJ_ROOT'
    def _before(self,context):
        self.root = res_utls.value(self.root)
        self.name = res_utls.value(self.name)

        context.prj = self
        prjdata = {}
        prjdata['PRJ_ROOT'] = self.root
        prjdata['PRJ_NAME'] = self.name
        utls.rg_var.import_dict(prjdata)
        safe_env_porp.ins().update(self.env.split(','))
    def _allow(self,context):
        return True



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
            rgio.struct_out("%-15s = %s" %(name,val),1)

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
        v = res_utls.value(self.value)
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
        value  = res_utls.value(self.value)
        expect = res_utls.value(self.expect)
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
    _name = ""

    def _allow(self,context):
        return True
    def _before(self,context):
        rg_logger.info("system:%s _before " %(self._name))
        utls.rg_var.keep()
        context.keep()

        #support run_path var
        auto_vars = vars()
        auto_vars.SYS_NAME = self._name
        auto_vars.RUN_PATH = "%s/run/%s" %(context.prj.root,self._name)

        run_path     = res.files.path()
        run_path.dst = auto_vars.RUN_PATH

        self.push(run_path)
        self.push(auto_vars)

    def _after(self,context):
        context.rollback()
        utls.rg_var.rollback()
        rg_logger.info("system:%s _after" %(self._name))

    def _resname(self):
        return self._name

    def _check(self,context):
        self._check_print(True,"system: %s" %self._name)
        interface.control_box._check(self,context)

    def _info(self,context):
        rgio.struct_out("system: %s" %(self._name))
        interface.control_box._info(self,context)


class prj_main(interface.control_box, interface.base) :
    """
    """
    _name = "main"
    def _allow(self,context):
        return True
    def _info(self,context):
        rgio.struct_out("rg: %s" %(self._name))
        interface.control_box._info(self,context)
    def _before(self,context):
        rg_logger.info("main: _before")

    def _after(self,context):
        rg_logger.info("main: _after")

class modul(interface.control_box,interface.base) :
    """
    !R.modul
        _name : "php-web"
        _res  :
            ...
    """
    _name = ""
    _sandbox = True
    def _resname(self):
        tag = self.__class__.__name__
        return tag
    def _info(self,context):
        rgio.struct_out("modul : %s" %(self._name))
        interface.control_box._info(self,context)

    def _before(self,context):
        # run_struct.push("modul %s" %(self._name))
        rg_logger.info("modul:%s _before" %(self._name))
        if self._sandbox:
            utls.rg_var.keep()
            context.keep()

    def _after(self,context):
        if self._sandbox:
            context.rollback()
            utls.rg_var.rollback()
        rg_logger.info("modul:%s _after" %(self._name))
        # run_struct.pop()

class using(interface.resource):
    """
    !R.using
      path  : "/usr/local/lib/rigger-ng/php.yaml"
      modul : "php-web"
      args  : !R.args
        PHP_INI : "php.ini"
    """
    path  = ""
    modul = ""
    args  = None
    def _allow(self,context):
        return True
    def _before(self,context):
        # run_struct.push("using.module.%s" %self.modul)
        self.path       = res_utls.value(self.path)
        if len(self.path) > 0 :
            node.module_load(self.path)
        key            = res_utls.value(self.modul)
        msg            = "load modul %s from '%s' failed! " %(key,self.path)
        module         = utls.check.not_none(node.module_find(key), msg)
        #需要deepcopy , 避免对module 的使用污染!
        self.modul_obj = copy.deepcopy(module)
        if self.args is not None :
            self.modul_obj.push(self.args)
        self.modul_obj._before(context)

    def _after(self,context):
        self.modul_obj._after(context)

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

class env(interface.control_box,interface.base):
    """

    """
    _mix      = None
    def _resname(self):
        return  "%s(%s)" %(self.__class__.__name__,self._name)
    def _info(self,context):
        rgio.struct_out("env: %s" %(self._name))
        interface.control_box._info(self,context)

    def _before(self,context):
        rg_logger.info("env:%s _before" %(self._name))
        if self._mix is not None :
            for key in  self._mix.split(",") :
                self.append(res.node.env_find(key))


        # vars._before(self,context)

    def _after(self,context):
        rg_logger.info("env:%s _after " %(self._name))
