#coding=utf8
import re,logging
import interface,utls.rg_var,utls.rg_json
import node
import utls.dbc , utls.check
import res.node
import copy
from utls.rg_io import  rgio , run_struct,rg_logger
from base import *
from utls.tpl.tpl_var import safe_env_porp

import  res.files

class project(interface.resource,res_utls) :
    """
    项目设定
    示例:
    - !R.project
        root : "${HOME}/devspace/rigger-ng/demo"
        name : "rg_demo"
    """
    root = ""
    name = ""
    env  = 'HOME,USER,PRJ_ROOT'

    def setup4start(self,context):
        self.root = res_utls.value(self.root)
        self.name = res_utls.value(self.name)
        context.prj = self

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
    定义变量
    !R.vars:
        _json : "/path/data.json:/xpath/a/b/c"
        A: 1
        B: "hello"
    """

    _json = None
    name = "vars"
    def depend_check(self,context) :
        pass

    def _allow(self,context):
        return True
    def vars_data(self):
        items    = self.__dict__
        json_key = '_json'

        if self._json is not None :
            jfile = res_utls.value(self._json)
            jargs = jfile.split(":")
            data  = utls.rg_json.load_file(jargs[0],jargs[1])
            items.update(data)
        if json_key in items :
            del items[json_key]

        return  items

    def _before(self,context):
        # import pdb
        # pdb.set_trace()
        vars_data = self.vars_data()
        for name , val in   vars_data.items():
            name= name.upper()
            rg_logger.debug("%s =%s" %(name,val))
            setattr(context,name,val)
        utls.rg_var.import_dict(vars_data)

    def add(self,key,value):
        self.__dict__[key] = value

    def _after(self,context):
        pass


    def _info(self,context,level):
        if  level  <= 0  :
            return
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
    !R.assert_eq
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
    _sys:
        - !R.system
            _name: "init"
            _limit :
                envs   : "demo,online"
                passwd : "rgisgood"
            _res:
                - !R.echo
                    value : "${PRJ_ROOT}"
    """
    _name   = ""
    _limit  = None

    def _allow(self,context):
        if self._limit is not None :
            for env in self._limit['envs'].split(","):
                if context.have_env(env)  and context.passwd != self._limit['passwd']:
                    rgio.struct_out("[ignore system] %s" %(self._name))
                    return False
        return True
    def _before(self,context):
        rg_logger.info("system:%s _before " %(self._name))
        utls.rg_var.keep()
        context.keep()

        #support run_path var
        auto_vars = vars()
        auto_vars.SYS_NAME = self._name
        auto_vars.RUN_PATH = "%s/run/%s" %(context.prj.root,self._name)
        context.run_path   = auto_vars.RUN_PATH

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

    def _info(self,context,level):
        rgio.struct_out("system: %s" %(self._name))
        interface.control_box._info(self,context,level)


class prj_main(interface.control_box, interface.base) :
    """
    """
    _name = "main"
    def _allow(self,context):
        return True
    def _info(self,context,level):
        rgio.struct_out("rg: %s" %(self._name))
        interface.control_box._info(self,context,level)
    def _before(self,context):
        rg_logger.info("main: _before")

    def _after(self,context):
        rg_logger.info("main: _after")


class include(interface.resource):
    """
    !R.include
        _path:
            - "a.yaml"
            - "b.yaml"
    """
    _path = None
    def _allow(self,context):
        return True
    def _before(self,context):
        import conf.run_conf
        for path in self._path  :
            if os.path.isfile(path) :
                path = res_utls.value(path)
                conf.run_conf.load(path)
            else:
                raise interface.rigger_exception("%s path not found! in !R.include" %path)


class modul(interface.control_box,interface.base) :
    """
    !R.modul
        _name : "php-web"
        _res  :
        _args :
            X : "ABC"
            ...
    """
    _name = ""
    _sandbox = True
    def _resname(self):
        tag = self.__class__.__name__
        return tag
    def _info(self,context,level):
        if  level  <= 0  :
            return
        rgio.struct_out("modul : %s" %(self._name))
        interface.control_box._info(self,context,level)

    def load_default_args(self):
        if hasattr(self,"_args") and isinstance(self._args,dict):
            args_vars = vars()
            for key,value in self._args.items() :
                args_vars.add(key,value)
            self.push(args_vars)
    def _before(self,context):
        rg_logger.info("modul:%s _before" %(self._name))
        if self._sandbox:
            utls.rg_var.keep()
            context.keep()
        self.load_default_args()

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
        self.path       = res_utls.value(self.path)
        if len(self.path) > 0 :
            node.module_load(self.path)
        key            = res_utls.value(self.modul)
        msg            = "load modul %s from '%s' failed! " %(key,self.path)
        module         = utls.check.not_none(node.module_find(key), msg)
        #需要deepcopy , 避免对module 的使用污染!
        self.modul_obj = copy.deepcopy(module)
        #压入传入数据
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

    def _info(self,context,level):
        if  level  <= 0  :
            return
        self.modul_obj._info(context,level)



class env(interface.control_box,interface.base):
    """

    _env:
        - !R.env
            _name : "dev"
            _mix  : "base, _dev"
            _res  :
                - !R.vars
                        DB_NAME : "rigger_db"
    """
    _mix      = None
    def _resname(self):
        return  "%s(%s)" %(self.__class__.__name__,self._name)
    def _info(self,context,level):
        rgio.struct_out("env: %s" %(self._name))
        interface.control_box._info(self,context,level)

    def _before(self,context):
        context.use_env(self._name)
        rg_logger.info("env:%s _before" %(self._name))
        mix_obj = []
        if self._mix is not None :
            for key in  self._mix.split(",") :
                obj =  interface.res_proxy(res.node.env_find,key,"env")
                mix_obj.append(obj)
                # obj = res.node.env_find(key)
                # if obj is None :
                #     raise interface.rigger_exception("env [%s] : mix [%s] not found " %(self._name,key))
                # self.append(obj)
        self.extend_left(mix_obj)



        # vars._before(self,context)

    def _after(self,context):
        rg_logger.info("env:%s _after " %(self._name))
