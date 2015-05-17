#coding=utf-8
import  os , string   , logging ,copy
import  interface,utls.rg_sh , utls.rg_var
from utls.rg_io  import rgio ,rg_logger
from res.base   import *
from string import Template



class shell(interface.resource,res_utls):
    """
    !R.shell:
        script : "/test.sh "
        args   : ""
        run    : "start"

    run =  conf | start |  stop
    """
    script = None
    args   = ""
    run    = "start"
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
    def doit(self,context,pos) :
        if self.run == pos :
            cmd = Template( self.script + "  $ARGS").substitute(
                    ARGS = self.args
                    )
            utls.rg_var.export_env()
            self.execmd(cmd)


    def _start(self,context) :
        self.doit(context,"start")
        pass
    def _stop(self,context) :
        self.doit(context,"stop")
        pass

class php(interface.resource,res_utls):
    """
    !R.php:
        ini    : "${PHP_INI}"
        script : "demo.php "
        args   : ""
        run    = "start"
    """
    bin    = "/usr/bin/php"
    ini    = ""
    script = None
    args   = ""
    run    = "start"
    def _before(self,context) :

        self.ini  = res_utls.value(self.ini)
        self.bin  = res_utls.value(self.bin)
        self.args = res_utls.value(self.args)
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


    def doit(self,context,pos) :
        if self.run != pos :
            return

        ini = self.ini
        if len(self.ini ) >=1 :
            ini =  " -c " + self.ini
        cmd = Template("$BIN  $INI " + self.script + "  $ARGS").substitute(
                BIN  = self.bin,
                INI  = ini,
                ARGS = self.args
                )
        utls.rg_var.export_env()
        self.execmd(cmd)


    def _start(self,context) :
        self.doit(context,"start")

    def _stop(self,context) :
        self.doit(context,"stop")
