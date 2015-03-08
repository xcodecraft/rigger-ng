#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args

_logger = logging.getLogger()

class files_tc(base.tc_tools.rigger_tc):

    def test_path(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_files.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            impl.rg_run.run_cmd("conf,clean -s path -e dev",conf)

        expect= """
            if test ! -e ${PRJ_ROOT}/run/test_1; then   mkdir -p ${PRJ_ROOT}/run/test_1 ; fi ;   chmod o+w  ${PRJ_ROOT}/run/test_1;
            if test ! -e ${PRJ_ROOT}/run/test_2; then   mkdir -p ${PRJ_ROOT}/run/test_2 ; fi ;   chmod o+w  ${PRJ_ROOT}/run/test_2;
            if test -e ${PRJ_ROOT}/run/test_1 ; then rm -rf  ${PRJ_ROOT}/run/test_1 ; fi ;
            if test -e ${PRJ_ROOT}/run/test_2 ; then rm -rf  ${PRJ_ROOT}/run/test_2 ; fi ;
            """
        # print(mock.cmds)
        self.assertMacroEqual( expect, mock.cmds)


