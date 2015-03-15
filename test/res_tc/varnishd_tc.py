#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args
_logger = logging.getLogger()

class varnish_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,cmd):
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_varnishd.yaml")
        mock = base.tc_tools.res_mock()
        with mock :
            impl.rg_run.run_cmd(cmd,conf)
        return mock.cmds

    def test_start(self) :
        result = self.asst_cmd("start -s varnishd -e dev")
        expect = """
        if ! test -s /home/maijunsheng/devspace/rigger-ng/varnishd_RG_UT_80.pid ; then sudo /usr/local/sbin/varnish -f /home/maijunsheng/devspace/rigger-ng/conf/used/local_cache.vcl -s malloc,20M -T 127.0.0.1:2000 -a 0.0.0.0:80 -P/home/maijunsheng/devspace/rigger-ng/varnishd_RG_UT_80.pid -n local_proxy_dev -w 100,1000,60 ; fi
        """
        self.assertMacroEqual(expect,result)

    def test_stop(self) :
        result = self.asst_cmd("stop -s varnishd -e dev")
        #self.assertMacroEqual(expect,result)
        print result

    def test_reload(self) :
        result = self.asst_cmd("reload -s varnishd -e dev")
        #self.assertMacroEqual(expect,result)
        print result

    def test_check(self) :
        result = self.asst_cmd("check -s varnishd -e dev")
        print result
        #self.assertMacroEqual(expect,result)

