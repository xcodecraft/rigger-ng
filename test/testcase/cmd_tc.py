#coding=utf8
import  logging
import  interface
from    tc_tools   import *
# from    impl.rg_cmd import *
from    impl.rg_args import *
import  impl.rg_cmd



_logger = logging.getLogger()

def parse_cmd(rargs,cmdstr) :
    parser = rarg_parser()
    parser.parse(rargs,cmdstr.split(' '))
    cmd = rargs.prj.cmds[0]
    return ins_cmd(cmd)

def ins_cmd(name) :
    cmds = dir(impl.rg_cmd)
    cmd  = "%s_cmd" %name
    if cmd in cmds :
        exec "obj = impl.rg_cmd.%s() " %cmd
        return obj
    return None


class cmd_tc(rigger_tc):
    def test_insobj(self) :
        rargs  = run_args()
        o = parse_cmd(rargs,"help")
        o._execute(rargs)
        rargs  = run_args()
        o = parse_cmd(rargs,"help res")
        o._execute(rargs)

        rargs  = run_args()
        o = parse_cmd(rargs,"help res echo")
        o._execute(rargs)
        # o._config()

