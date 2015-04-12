#coding=utf8
import  utls.tpl ,utls.rg_var,interface ,base.tc_tools
import  res
import  res.node
import  impl.rg_run
from base.tc_tools import *



class inner_tc(rigger_tc):
    def setUp(self):
        self.conf = path_of_prj("/test/res_tc/res_modul.yaml")

    def test_modul(self) :
        res.node.module_load(self.conf)
        m       = res.node.module_find("m1")
        self.assertMacroEqual(m._name,"m1")
    def test_using(self):
        u       = res.using()
        u._name = "using"
        u.path  = self.conf
        u.modul = "m1"
        context = interface.run_context()
        u._before(context)
        u._config(context)
    def test_muti_module(self):
        u       = res.using()
        u._name = "using"
        u.path  = self.conf
        u.modul = "m2"
        context = interface.run_context()
        u._before(context)
        u._config(context)

class  muti_env_tc(rigger_tc) :

    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_env(self) :
        conf = path_of_prj("/test/res_tc/muti_env.yaml")
        self.asst_cmd(conf,"conf -s test -e dev")
        self.asst_cmd(conf,"conf -s test -e _test,base")
        self.asst_cmd(conf,"conf -s test -e _dev,_test,base")
