#coding=utf8
import  logging
import  interface
from    tc_tools   import *
# from    impl.rg_cmd import *
from    impl.rg_args import *
import  impl.rg_run



_logger = logging.getLogger()



class cmd_tc(rigger_tc):
    def asst_cmd(self,cmd):
        impl.rg_run.run_cmd(cmd)
    def test_insobj(self) :
        self.asst_cmd("help")
        self.asst_cmd("help res")
        self.asst_cmd("help res echo ")

    def test_conf(self):
        self.asst_cmd("conf -s test -o dev ")

