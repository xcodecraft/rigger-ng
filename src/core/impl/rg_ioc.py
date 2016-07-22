#coding=utf-8
import logging
import interface
import utls.rg_io

from utls.rg_io import rg_logger


def setup() :
    interface.regist_res("project,env,system,modul,prj_main,using",     "res.inner")
    interface.regist_res("env,system,modul,prj_main,using,include",     "res.inner")
    interface.regist_res("echo,vars,assert_eq",                         "res.inner")

    interface.regist_res("copy,link,path,file_merge,intertpl,file_tpl", "res.files")

    interface.regist_res("cmd,php,shell",                               "res.shell")

    interface.regist_cmd("check,clean,info",                            "impl.rg_cmd.rg_cmd_prj")
    interface.regist_cmd("conf,reconf,start,stop,restart,reload",  "impl.rg_cmd.rg_cmd_prj")
    interface.regist_cmd("help,init,tpl",                               "impl.rg_cmd.rg_cmd")
    interface.regist_cmd("php,shell,phpunit",                                   "impl.rg_cmd.rg_cmd_prj")
    interface.regist_cmd("ci,rc,sonar",                                 "impl.rg_cmd.rg_cmd_dev")
    interface.regist_conf("git,project,version,sonar",                  "conf.dev_conf")

def list_res() :
    import  res
    sorted_res = sorted(interface.registed_resource)
    for name in sorted_res :
        code = "obj = res.%s()" %(name)
        rg_logger.debug("exec code : %s" %code)
        try :
            exec code
            utls.rg_io.export_objdoc(name,obj )
        except  Exception as e :
            raise interface.rigger_exception("@list_res() code error: %s \n %s" %(code,e) )



def ins_res(name) :
    import  res
    for res_name,module in interface.registed_resource.items() :
        if  res_name == name :
            code = "obj = res.%s()" %(name)
            rg_logger.debug("exec code : %s" %code)
            try :
                exec code
                return obj
            except  Exception as e :
                raise interface.rigger_exception("@ins_res() code error: %s \n %s" %(code,e) )
    return None


def list_cmd() :
    import  impl.rg_cmd
    for name in interface.cmds_index :
        code = "obj = impl.rg_cmd.%s_cmd()" %(name)
        rg_logger.debug("exec code : %s" %code)
        try :
            exec code
            utls.rg_io.export_objdoc(name,obj )
        except  Exception as e :
            raise interface.rigger_exception("@list_cmd() code error: %s \n %s" %(code,e) )



def ins_cmd(name) :
    import  impl.rg_cmd
    for cmd,module in interface.registed_cmd.items() :
        if  cmd == name :
            code = "obj = impl.rg_cmd.%s_cmd()" %(name)
            rg_logger.debug("exec code : %s" %code)
            try :
                exec code
                return obj
            except  Exception as e :
                raise interface.rigger_exception("@ins_cmd() code error: %s \n %s" %(code,e) )
    # return None
    raise interface.rigger_exception(" '%s' cmd not support!" %(name) )
