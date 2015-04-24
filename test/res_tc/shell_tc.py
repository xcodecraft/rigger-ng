#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args

_logger = logging.getLogger()

class shell_tc(base.tc_tools.rigger_tc):
    def setUp(self):
        self.conf = utls.rg_var.value_of("${PRJ_ROOT}/test/res_tc/shell_res.yaml")

    def test_shell(self) :
        # mock = base.tc_tools.res_mock()
        # with   mock :
        impl.rg_run.run_cmd("conf,start -s shell -e dev,base",self.conf)

