#coding=utf8
import  logging
import  utls.tpl ,interface ,tc_tools
import  impl.rg_args
# from impl.rg_args import *


_logger = logging.getLogger()



class mysql_tc(tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_mysql(self) :
        conf   = impl.rg_var.value_of("${HOME}/devspace/rigger-ng/test/data/res_mysql.yaml")
        with  tc_tools.res_mock as mock :
            self.asst_cmd(conf,"data -s mysql -e dev")

