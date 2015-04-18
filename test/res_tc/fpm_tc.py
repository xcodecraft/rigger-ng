#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args
_logger = logging.getLogger()

class fpm_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,cmd):
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_fpm.yaml")
        mock = base.tc_tools.res_mock()
        with mock :
            impl.rg_run.run_cmd(cmd,conf)
        return mock.cmds

    def test_config(self) :
        result = self.asst_cmd("start -s fpm -e dev,base")
        expect = """
        """
        print result

    def test_start(self) :
        result = self.asst_cmd("start -s fpm -e dev,base")
        expect = """
        """
        print result

    def test_stop(self) :
        result = self.asst_cmd("stop -s fpm -e dev,base")
        expect = """
        """
        print result

    def test_check(self) :
        #result = self.asst_cmd("check -s fpm -e dev")
        expect = """
        """
        #print result

    def test_reload(self) :
        result = self.asst_cmd("reload -s fpm -e dev,base")
        expect = """
        """
        print result

    def test_restart(self) :
        result = self.asst_cmd("restart -s fpm -e dev,base")
        expect = """
        """
        print result


class fpm_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,cmd):
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_fpm.yaml")
        mock = base.tc_tools.res_mock()
        with mock :
            impl.rg_run.run_cmd(cmd,conf)
        return mock.cmds

    def test_restart(self) :
        # result = self.asst_cmd("restart -s fpm -e dev,base")
        expect = """
        """
