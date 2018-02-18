
#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_run
import  impl.rg_utls
import  time
import  setting

_logger = logging.getLogger()

class check_tc(base.tc_tools.rigger_tc):
    def setUp(self):
        self.conf = utls.rg_var.value_of("${PRJ_ROOT}/src/extends/res/check/test/check.yaml")


    def test_check(self) :
        setting.debug       = True
        impl.rg_run.run_cmd("conf,start,check -s check -e dev -d 1",self.conf)
        impl.rg_run.run_cmd("clean",self.conf)


