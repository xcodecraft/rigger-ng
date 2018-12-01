#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_run
import  impl.rg_utls
import  time
import  setting

_logger = logging.getLogger()

class port_tc(base.tc_tools.rigger_tc):
    def setUp(self):
        self.conf = utls.rg_var.value_of("${PRJ_ROOT}/src/extends/res/websys/tc/port_res.yaml")

    def test_crontab(self) :
        setting.debug       = True
        self.assert_cmd("conf,start -s crontab -e dev,base -d 1") 
        self.assert_cmd("conf,stop  -s crontab -e dev,base -d 1")

    def test_hosts(self) :
        setting.debug       = True
        self.assert_cmd("conf -s hosts -e dev,base -d 1")
        self.assert_cmd("clean -s hosts -e dev,base -d 1")


    def test_varnish(self) :
        mock = base.tc_tools.res_mock()
        with   mock :
            self.assert_cmd("conf,start  -s varnishd -e dev,base ")
            self.assert_cmd("conf,reload,check -s varnishd -e dev,base  ")
            self.assert_cmd("conf,stop   -s varnishd -e dev,base ")
