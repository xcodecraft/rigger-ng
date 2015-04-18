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
if test ! -e ${PRJ_ROOT}/run/nginx_conf; then   mkdir -p ${PRJ_ROOT}/run/nginx_conf ; fi ;   chmod o+w  ${PRJ_ROOT}/run/nginx_conf;
chmod o+w ${PRJ_ROOT}/test/data/websvc/nginx_src.conf
if ! test -L /etc/nginx/sites-enabled/rigger-tc_nginx_conf_${USER}.conf ; then   dirname /etc/nginx/sites-enabled/rigger-tc_nginx_conf_${USER}.conf | xargs mkdir -p ;  ln -s   ${PRJ_ROOT}/test/data/websvc/nginx_src.conf /etc/nginx/sites-enabled/rigger-tc_nginx_conf_${USER}.conf ; fi;
/usr/sbin/service nginx reload
        """

        # print("\n")
        # print mock.cmds
        # print expect
        self.assertMacroEqual(expect, mock.cmds)
