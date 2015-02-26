#coding=utf-8
import string , logging, sys
import interface
# import rg_io ,rg_sh
_logger = logging.getLogger()

import rg_cmd,rg_args , impl.rg_cmd_prj


def run_cmd( cmdstr,yaml_conf=None) :
    rargs  = rg_args.run_args()
    parser = rg_args.rarg_parser()
    parser.parse(rargs,cmdstr.split(' '))
    if yaml_conf is not None:
        rargs.prj.conf = yaml_conf

    #TODO: muti cmd support
    cmd    = rargs.prj.cmds[0]
    obj    = ins_cmd(cmd)
    obj._config(parser.argv,rargs)
    obj._execute(rargs)



def ins_cmd_model(name,model,obj):
    cmds = dir(model)
    cmd  = "%s_cmd" %name
    if cmd in cmds :
        exec "xobj = %s.%s() " %(model.__name__,cmd)
        return xobj
    return None

def ins_cmd(name) :
    obj = None
    obj = ins_cmd_model(name,impl.rg_cmd_prj,obj)
    if obj is not None :
        return obj
    obj = ins_cmd_model(name,impl.rg_cmd,obj)
    if obj is not None :
        return obj
    return obj
