#coding=utf8
import  utls.tpl ,utls.rg_var,interface ,base.tc_tools
import  res
import  res.modules



class inner_tc(base.tc_tools.rigger_tc):
    def setUp(self):
        self.conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_modul.yaml")

    def test_modul(self) :
        res.modules.load(self.conf)
        m       = res.modules.find("m1")
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
