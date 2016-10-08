#coding=utf-8
import  os , string   , logging ,copy
import  interface,utls.rg_sh , utls.rg_var
from utls.rg_io  import rgio ,rg_logger
from res.base   import *
from string import Template


class cmd(interface.resource,res_utls) :
    """
    """
    cmd = ""
    run = "start"
    def _before(self,context) :
        self.cmd= res_utls.value(self.cmd)
        self.run= res_utls.value(self.run)
        pass

    def _start(self,context) :
        self.doit(context,"start")
        pass
    def _reload(self,context) :
        self.doit(context,"reload")
        pass

    def _stop(self,context) :
        self.doit(context,"stop")
        pass

    def doit(self,context,pos) :
        if  pos in self.run.split(","):
            self.execmd(self.cmd)



class shell(interface.resource,res_utls):
    """
    !R.shell:
        script : "/test.sh "
        args   : ""
        run    : "start"

    run =  conf,start,stop
    """
    script = None
    args   = ""
    run    = "start"
    def _before(self,context) :
        self.env_keep = copy.copy(os.environ)
        self.script = res_utls.value(self.script)
        self.args   = res_utls.value(self.args)

    def _after(self,context) :
        if self.env_keep is not None :
            os.environ = copy.copy(self.env_keep)
    def doit(self,context,pos) :
        if not os.path.exists(self.script) :
            raise interface.rigger_exception( "script is bad! %s " %(self.script))
        if  pos in self.run.split(","):
            cmd = Template( self.script + "  $ARGS").substitute(
                    ARGS = self.args
                    )
            utls.rg_var.export_env()
            self.execmd(cmd)

    def _config(self,context) :
        self.doit(context,"conf")
        pass

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
    bin    = "${PHP_BIN}"
    ini    = "${PHP_INI}"
    script = None
    args   = ""
    run    = "start"
    def _before(self,context) :
        with res_context(self.__class__.__name__) :
            self.ini    = res_utls.value(self.ini)
            self.bin    = res_utls.value(self.bin)
            self.args   = res_utls.value(self.args)
            self.script = res_utls.value(self.script)

        self.env_keep = None
        self.env_keep = copy.copy(os.environ)
        return
    def _after(self,context) :
        if self.env_keep is not None :
            os.environ = copy.copy(self.env_keep)


    def doit(self,context,pos) :
        if len(self.script) == 0 :
            return
        self.must_exists(self.ini)
        self.must_exists(self.bin)
        self.must_exists(self.script)
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
    def _data(self,context) :
        self.doit(context,"data")
