#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args

_logger = logging.getLogger()

class files_tc(base.tc_tools.rigger_tc):
    def setUp(self):
        self.conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_files.yaml")

    def test_path(self) :
        mock = base.tc_tools.res_mock()
        with   mock :
            impl.rg_run.run_cmd("conf,clean -s path -e dev",self.conf)

        expect= """
            if test ! -e ${PRJ_ROOT}/run/test_1; then   mkdir -p ${PRJ_ROOT}/run/test_1 ; fi ;   chmod o+w  ${PRJ_ROOT}/run/test_1;
            if test ! -e ${PRJ_ROOT}/run/test_2; then   mkdir -p ${PRJ_ROOT}/run/test_2 ; fi ;   chmod o+w  ${PRJ_ROOT}/run/test_2;
            if test -e ${PRJ_ROOT}/run/test_1 ; then rm -rf  ${PRJ_ROOT}/run/test_1 ; fi ;
            if test -e ${PRJ_ROOT}/run/test_2 ; then rm -rf  ${PRJ_ROOT}/run/test_2 ; fi ;
            """
        # print(mock.cmds)
        self.assertMacroEqual( expect, mock.cmds)

    def test_tpl(self) :
        mock = base.tc_tools.res_mock()
        with   mock :
            impl.rg_run.run_cmd("conf,clean  -s tpl -e dev",self.conf)
        # print(mock.cmds)
        expect= """
        chmod o+w ${PRJ_ROOT}/test/data/files/prj_use.yaml
        if test -e ${PRJ_ROOT}/test/data/files/prj_use.yaml ; then rm -rf  ${PRJ_ROOT}/test/data/files/prj_use.yaml ; fi
        """
        self.assertMacroEqual( expect, mock.cmds)


