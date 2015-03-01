#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args
_logger = logging.getLogger()

class mysql_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_mysql(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_mysql.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"data -s mysql -e dev")

        expect = """
        /usr/bin/mysql -hlocalhost -uroot -p  -e "DROP DATABASE IF EXISTS ;CREATE DATABASE  DEFAULT CHARACTER SET UTF8;"
        /usr/bin/mysql -hlocalhost  -u -p < ${PRJ_ROOT}/test/data/init.sql
        """
        self.assertMacroEqual( expect, mock.cmds)
        # print(mock.cmds)

