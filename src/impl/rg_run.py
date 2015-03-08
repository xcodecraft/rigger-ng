#coding=utf-8
import string , logging, sys
import interface, rg_args, rg_ioc
from utls.rg_io import rg_logger

def run_cmd(cmdstr,yaml_conf=None) :
    rargs  = rg_args.run_args()
    parser = rg_args.rarg_parser()
    parser.parse(cmdstr.split(' '))
    rargs.parse_update(parser)
    if yaml_conf is not None:
        rargs.prj.conf = yaml_conf

    run_rigger(rargs,parser.argv)

def run_rigger(rargs, argv) :
    #TODO: muti cmd support
    if len(rargs.prj.cmds) == 0 :
        raise interface.rigger_exception("No Cmd!")
    cmds = rargs.prj.cmds[0]
    for  cmd in cmds.split(',') :
        obj = rg_ioc.ins_cmd(cmd)
        if obj is None :
            raise  interface.rigger_exception( "unfound '%s' cmd instance" %cmd)
        rg_logger.info("cmd: %s , cmd_ins : %s" %(cmd,obj.__class__.__name__))
        obj._config(argv,rargs)
        obj._execute(rargs)




