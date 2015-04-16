import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args
import  os

class websvc_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)
    def test_nginx(self) :
        conf = utls.rg_var.value_of("${PRJ_ROOT}/test/res_tc/websvc_res.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"conf,start -s nginx_conf -e dev  ")

        expect="""
chmod o+w ${PRJ_ROOT}/test/data/websvc/nginx_src.conf
if ! test -L ${PRJ_ROOT}/test/data/websvc/nginx_dst.conf ; then   dirname ${PRJ_ROOT}/test/data/websvc/nginx_dst.conf | xargs mkdir -p ;  ln -s   ${PRJ_ROOT}test/data/websvc/nginx_dst.conf ${PRJ_ROOT}test/data/websvc/nginx_dst.conf ; fi;
        """

        print mock.cmds
        # self.assertMacroEqual(expect, mock.cmds)
