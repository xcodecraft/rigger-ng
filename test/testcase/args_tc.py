#coding=utf8
import  logging
import  utls.tpl ,interface ,tc_tools
from impl.rg_args import *


_logger = logging.getLogger()



class args_tc(tc_tools.rigger_tc):
    def test_parse(self) :
        rargs  = run_args()
        parser = rarg_parser()
        cmd    = "conf -o diy -s test"
        parser.parse(rargs,cmd.split(' '))
        self.assertEqual(str(rargs),cmd )


        rargs  = run_args()
        cmd    = "start -o ubuntu -s api"
        parser.parse(rargs,cmd.split(' '))
        self.assertEqual(str(rargs),cmd )
