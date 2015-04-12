import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args
import  os

class pylon_autoload_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_pylon_autoload(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_pylon_autoload.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"conf -s pylon_autoload -e dev ")

        expect="""echo "" > ${HOME}/devspace/rigger-ng/run/pylon_autoload/autoload/_find_cls.tmp
        find ${HOME}/devspace/rigger-ng/ -name "*.php"   |  xargs  grep  -H -i -E "^ *(abstract)? *class "  >> ${HOME}/devspace/rigger-ng/run/pylon_autoload/autoload/_find_cls.tmp
        find ${HOME}/devspace/rigger-ng/ -name "*.php"   |  xargs  grep  -H -i -E "^ *interface "  >> ${HOME}/devspace/rigger-ng/run/pylon_autoload/autoload/_find_cls.tmp
        sort ${HOME}/devspace/rigger-ng/run/pylon_autoload/autoload/_autoload_clspath.tmp > ${HOME}/devspace/rigger-ng/run/pylon_autoload/autoload/_autoload_clspath.idx; rm ${HOME}/devspace/rigger-ng/run/pylon_autoload/autoload/_autoload_clspath.tmp
        sort ${HOME}/devspace/rigger-ng/run/pylon_autoload/autoload/_autoload_clsname.tmp > ${HOME}/devspace/rigger-ng/run/pylon_autoload/autoload/_autoload_clsname.idx; rm ${HOME}/devspace/rigger-ng/run/pylon_autoload/autoload/_autoload_clsname.tmp
        """

        # print mock.cmds
        self.assertMacroEqual(expect, mock.cmds)

