#coding=utf-8
import logging
import interface
import time
import random

from utls.rg_io  import rgio,rg_logger
from utls.rg_var import value_of
from utls.rg_sh  import shexec,check_proc
from impl.rg_utls import *
from string     import *
from res.base   import *
import utls.check

class daemon_base(interface.resource,res_utls):

    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.script     = res_utls.value(self.script)
            self.logpath    = res_utls.value(self.logpath)
            self.runpath    = res_utls.value(self.runpath)
            self.zdaemon    = res_utls.value(self.zdaemon)
            self.confpath   = res_utls.value(self.confpath)
            self.tag        = res_utls.value(self.tag)
            self.worker     = int(res_utls.value(self.worker))
            self.main_ukey  = self.tag
            self.ukeys      = {}
            self.confs      = {}

        for i in range(1,self.worker + 1 ):
            self.confs[i]       = self.confpath +  "/zdaemon-%s-%d.xml" %(self.main_ukey,i)
            self.ukeys[i]       = "%s_%d" %(self.main_ukey,i)
        self.program    = self.script

    def _config(self,context):
        for i in range(1,self.worker + 1):
            self.build_conf(self.ukeys[i],self.confs[i])

    def _depend(self,m,context):
        m.check_exists(self.python)
        m.check_exists(self.zdaemon)

    def _start(self,context):
        cmd_tpl = "$ZDAEMON  -C $CONF  start "
        for i in range(1,self.worker + 1):
            conf = self.confs[i]
            cmd  = Template(cmd_tpl).substitute( ZDAEMON = self.zdaemon,CONF= conf)
            print(cmd)
            # print ("start: " + self.program)
            self.execmd(cmd)

    def _stop(self,context):
        cmd_tpl = "$ZDAEMON  -C $CONF  stop "
        for i in range(1,self.worker + 1):
            conf = self.confs[i]
            cmd  = Template(cmd_tpl).substitute( ZDAEMON = self.zdaemon,CONF= conf)
            self.execmd(cmd)
    def _check(self,context):
        cmd_tpl = "ps auxww | grep zdaemon | grep  $CONF  | grep -v 'grep' "
        for i in range(1,self.worker + 1):
            conf = self.confs[i]
            cmd     = Template(cmd_tpl).substitute(CONF= os.path.basename(conf))
        check_proc("zdaemon",cmd)
#       program 太长。。。
        print ("program:" +  self.program)
        main_cmd =  ""
        for sub in self.program.split(' '):
            if len(sub) > len(main_cmd):
                main_cmd = sub
        cmd = Template("""ps auxww | grep -v "grep" | grep "$PROG" """).substitute(PROG= main_cmd )
        check_proc("daemon_prog ",cmd)

    def build_conf(self,ukey,conf):
        content = """
<runner>
    program         $SCRIPT
    backoff-limit   10
    daemon          $DAEMON
    forever         $FOREVER
    exit-codes      0,2
    umask           022
    directory       .
    default-to-interactive True
    hang-around     False
    transcript      $LOG/zout.log.$UK
    socket-name     $RUN_PATH/$UK.zsock
</runner>

<eventlog>
    level info
    <logfile>
    path $LOG/zrun.log.$UK
    </logfile>
</eventlog>

<environment>
 $ENVS
</environment>
"""
        envstr = ""
        if  not ( "hostname" in os.environ    or "HOSTNAME" in os.environ ) :
            import socket
            host = socket.gethostname()
            os.environ['hostname'] = host

        target= dict()
        utls.rg_var.export2dict(target)

        for k,v in target.items() :
            v = res_utls.value(v)
            envstr = envstr + "\t%s %s \n" %(k.upper() , v)


        # logpath = self.runpath  +  "/" + self.logpath;
        c = Template(content).substitute(SCRIPT=self.program, DAEMON=self.daemon,
                FOREVER=self.forever,LOG=self.logpath,UK=ukey,RUN_PATH=self.runpath,ENVS=envstr)
        # _logger.info("zdemon conf:")
        # _logger.info(c)
        if not os.path.exists(self.logpath) :
            self.execmd(" mkdir -p " + self.logpath)
        with  open(conf ,'w') as f :
            f.write(c)

class daemon_base_php(daemon_base):
    """
    示例:
    !R.daemon_php 
        script : "${PRJ_ROOT}/src/apps/console/work.php"
    """
    php_ini  = "${PHP_INI}"
    php_bin  = "${PHP_BIN}"
    script   = ""
    daemon   = "True"
    umask    = "022"
    forever  = "True"
    logpath  = "${RUN_PATH}"
    runpath  = "${RUN_PATH}"
    worker   = 1

    def _before(self,context):
        with res_context(self.__class__.__name__) :
            daemon_base._before(self,context)
            self.php_ini    = res_utls.value(self.php_ini)
            self.php_bin    = res_utls.value(self.php_bin)
            self.program    = "%s -c %s -f %s " %(self.php_bin,self.php_ini,self.script)
