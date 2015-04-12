#coding=utf8
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args
import  os

class pylon_router_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_pylon_router(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_pylon_router.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"conf -s pylon_router -e dev")
        # print(mock.cmds)
        expect = """grep --include "*.php" -i  -E "class .+ implements XService"  -R ${HOME}/devspace/rigger-ng/test/data/   |  sed -r "s/.+:class\s+(\S+)\s+.+\/\/\@REST_RULE:\s+(.+)/\\2 : \\1/g"  > ${HOME}/devspace/rigger-ng/run/pylon_router/router/_router.idx
        """
        self.assertMacroEqual(expect, mock.cmds)
