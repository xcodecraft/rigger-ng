#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
from impl.rg_args import *


_logger = logging.getLogger()



class args_tc(base.tc_tools.rigger_tc):
    def test_parse(self) :
        rargs  = run_args()
        parser = rarg_parser()
        cmd    = "conf -e dev -s test"
        parser.parse(rargs,cmd.split(' '))
        self.assertEqual(str(rargs),cmd )


        rargs  = run_args()
        cmd    = "start -e dev -s api"
        parser.parse(rargs,cmd.split(' '))
        self.assertEqual(str(rargs),cmd )
