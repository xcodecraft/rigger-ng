#coding=utf-8
import string , logging, sys
import interface
# import rg_io ,rg_sh
_logger = logging.getLogger()

import rg_cmd,rg_args


def run_cmd( cmdstr) :
    rargs  = rg_args.run_args()
    parser = rg_args.rarg_parser()
    parser.parse(rargs,cmdstr.split(' '))

    cmd    = rargs.prj.cmds[0]
    obj    = ins_cmd(cmd)
    obj._config(parser.argv,rargs)
    obj._execute(rargs)



def ins_cmd(name) :
    cmds = dir(rg_cmd)
    cmd  = "%s_cmd" %name
    if cmd in cmds :
        exec "obj = rg_cmd.%s() " %cmd
        return obj
    return None
