import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args , impl.rg_run
import  os

class pylon_autoload_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_pylon_autoload(self) :
        conf = utls.rg_var.value_of("${PRJ_ROOT}/extends/res/pylon/pylon_res.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"conf -s pylon_autoload -e dev ")

        expect="""echo "" > ${PRJ_ROOT}/run/pylon_autoload/autoload/_find_cls.tmp
        find ${PRJ_ROOT}/ -name "*.php"   |  xargs  grep  -H -i -E "^ *(abstract)? *class "  >> ${PRJ_ROOT}/run/pylon_autoload/autoload/_find_cls.tmp
        find ${PRJ_ROOT}/ -name "*.php"   |  xargs  grep  -H -i -E "^ *interface "  >> ${PRJ_ROOT}/run/pylon_autoload/autoload/_find_cls.tmp
        sort ${PRJ_ROOT}/run/pylon_autoload/autoload/_autoload_clspath.tmp > ${PRJ_ROOT}/run/pylon_autoload/autoload/_autoload_clspath.idx; rm ${PRJ_ROOT}/run/pylon_autoload/autoload/_autoload_clspath.tmp
        sort ${PRJ_ROOT}/run/pylon_autoload/autoload/_autoload_clsname.tmp > ${PRJ_ROOT}/run/pylon_autoload/autoload/_autoload_clsname.idx; rm ${PRJ_ROOT}/run/pylon_autoload/autoload/_autoload_clsname.tmp
        """

        # print mock.cmds
        self.assertMacroEqual(expect, mock.cmds)

class pylon_router_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_pylon_router(self) :
        conf = utls.rg_var.value_of("${PRJ_ROOT}/extends/res/pylon/pylon_res.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"conf -s pylon_router -e dev")
        # print(mock.cmds)
        expect = """grep --include "*.php" -i  -E "class .+ implements XService"  -R ${PRJ_ROOT}/test/data/   |  sed -r "s/.+:class\s+(\S+)\s+.+\/\/\@REST_RULE:\s+(.+)/\\2 : \\1/g"  > ${PRJ_ROOT}/run/pylon_router/router/_router.idx
        """
        self.assertMacroEqual(expect, mock.cmds)
