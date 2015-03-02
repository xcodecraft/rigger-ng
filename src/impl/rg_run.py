#coding=utf-8
import string , logging, sys
import interface
_logger = logging.getLogger()

import rg_args, rg_cmd, rg_ioc


def run_cmd(cmdstr,yaml_conf=None) :
    rargs  = rg_args.run_args()
    parser = rg_args.rarg_parser()
    parser.parse(rargs,cmdstr.split(' '))
    if yaml_conf is not None:
        rargs.prj.conf = yaml_conf

    run_rigger(rargs,parser.argv)

def run_rigger(rargs, argv) :
    #TODO: muti cmd support
    cmd = rargs.prj.cmds[0]
    obj = rg_ioc.ins_cmd(cmd)
    if obj is None :
        raise  interface.rigger_exception( "unfound '%s' cmd instance" %cmd)
    _logger.info("cmd: %s , cmd_ins : %s" %(cmd,obj.__class__.__name__))
    obj._config(argv,rargs)
    obj._execute(rargs)




