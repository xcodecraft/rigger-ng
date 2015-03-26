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
        sed = """sed -r "s/.+:class\s+(\S+)\s+.+\/\/\@REST_RULE:\s+(.+)/\\2 : \\1/g" """
        expect = """grep --include "*.php" -i  -E "class .+ implements XService"  -R ${PRJ_ROOT}/test/data/   |  """  +  sed + " > ${PRJ_ROOT}/test/data/_rest_conf.idx "
        self.assertMacroEqual(expect, mock.cmds)

        data = self.macro_data(expect.split('\n'))
        filename = 'rest_test.sh';
        with open(filename, 'w') as f:
               f.write(data[0])
        os.system('sh '+filename)
        os.system('rm '+filename)

        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"clean -s pylon_router -e dev")
        expect = "if test -e ${PRJ_ROOT}/test/data/_rest_conf.idx ; then rm -f  ${PRJ_ROOT}/test/data/_rest_conf.idx ; fi ; "
        self.assertMacroEqual(expect, mock.cmds)
