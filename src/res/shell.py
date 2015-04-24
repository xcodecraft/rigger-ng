#coding=utf-8
import  os , string   , logging ,copy
import  interface,utls.rg_sh , utls.rg_var
from utls.rg_io  import rgio ,rg_logger
from res.base   import *



class shell(interface.resource,res_utls):
    """
    !R.shell:
        script : "/test.sh"
    """
    script = None
    def _before(self,context) :
        self.env_keep = None
        if self.script is not None :
            self.script = res_utls.value(self.script)
            if os.path.exists(self.script) :
                self.env_keep = copy.copy(os.environ)
                return


        raise interface.rigger_exception( "script is bad! %s " %(self.script))
    def _after(self,context) :
        if self.env_keep is not None :
            os.environ = copy.copy(self.env_keep)

    def _start(self,context) :

        utls.rg_var.export_env()
        self.execmd(self.script + " _start")
        pass
    def _stop(self,context) :
        self.execmd(self.script + " _stop")
        pass

class php(interface.resource,res_utls):
    """
    !R.php:
        ini    : "${PHP_INI}"
        script : "/test.sh"
    """
    ini    = ""
    script = None
    def _before(self,context) :

        self.ini = res_utls.value(self.ini)
        self.env_keep = None
        if self.script is not None :
            self.script = res_utls.value(self.script)
            if os.path.exists(self.script) :
                self.env_keep = copy.copy(os.environ)
                return


        raise interface.rigger_exception( "script is bad! %s " %(self.script))
    def _after(self,context) :
        if self.env_keep is not None :
            os.environ = copy.copy(self.env_keep)

    def phpcmd(self,context) :
        if len(self.ini) >= 1 :
            cmd = "%s -c %s %s " %(context.php_def.bin, self.ini,self.script)
        else:
            cmd = "%s %s " %(context.php_def.bin, self.script)
        return cmd


    def _start(self,context) :

        utls.rg_var.export_env()
        cmd = " %s _start" %(self.phpcmd(context))
        self.execmd(cmd)
    def _stop(self,context) :
        utls.rg_var.export_env()
        cmd = " %s _stop" %(self.phpcmd(context))
        self.execmd(cmd)
