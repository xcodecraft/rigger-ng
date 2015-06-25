#coding=utf-8
import logging
import interface
import time
import random

from utls.rg_io  import rgio,rg_logger
from utls.rg_var import value_of
from utls.rg_sh  import shexec
from impl.rg_utls import *
from string     import *
from res.base   import *
import utls.check

class daemon_base(interface.resource):

    def _before(self,context):
        self.script     = res_utls.value(self.script)
        self.logpath    = res_utls.value(self.logpath)
        self.runpath    = res_utls.value(self.runpath)
        self.zdaemon    = res_utls.value(self.zdaemon)
        self.python     = res_utls.value(self.python)
        self.worker     = int(res_utls.value(self.worker))
        if not self.__dict__.has_key("main_ukey"):
            import hashlib
            self.main_ukey  = hashlib.md5(self.script +self.runpath ).hexdigest()
        self.ukeys      = {}
        self.confs      = {}

        for i in range(1,self.worker + 1 ):
            self.confs[i]       = self.runpath +  "/zdaemon-%d-%s.xml" %(i, self.main_ukey)
            self.ukeys[i]       = "%s_%d" %(self.main_ukey,i)
        self.program    = self.script
    def _config(self,context):
        for i in range(1,self.worker + 1):
            self.build_conf(self.ukeys[i],self.confs[i])

    def _depend(self,m,context):
        m.check_exists(self.python)
        m.check_exists(self.zdaemon)

    def _start(self,context):
        cmd_tpl = "$PYTHON  $ZDAEMON  -C $CONF  start "
        for i in range(1,self.worker + 1):
            conf = self.confs[i]
            cmd  = Template(cmd_tpl).substitute(PYTHON=self.python ,
                    ZDAEMON = self.zdaemon,CONF= conf)
            print ("start: " + self.program)
            rg_sh.shexec.execmd(cmd)

    def _stop(self,context):
        cmd_tpl = "$PYTHON  $ZDAEMON  -C $CONF  stop "
        for i in range(1,self.worker + 1):
            conf = self.confs[i]
            cmd  = Template(cmd_tpl).substitute(PYTHON=self.python ,
                    ZDAEMON = self.zdaemon,CONF= conf)
            rg_sh.shexec.execmd(cmd)
#     def _check(self,context):
#         cmd_tpl = "ps auxww | grep zdaemon | grep  $CONF  | grep -v 'grep' "
#         for i in range(1,self.worker + 1):
#             conf = self.confs[i]
#             cmd     = Template(cmd_tpl).substitute(CONF= os.path.basename(conf))
#         check_proc("zdaemon",cmd)
# #       program 太长。。。
#         print ("program:" +  self.program)
#         main_cmd =  ""
#         for sub in self.program.split(' '):
#             if len(sub) > len(main_cmd):
#                 main_cmd = sub
#         cmd = Template("""ps auxww | grep -v "grep" | grep "$PROG" """).substitute(PROG= main_cmd )
#         check_proc("daemon_prog ",cmd)

    # def export_env(self,context) :
        # with   open(self.env,'w') as efile :
        #     for  k ,v in target.items() :
        #         v = res_utls.value(v)
        #         efile.write( "env[%s] = %s \n" %(k,v))
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
    socket-name     $RUN_PATH/$UK.sock
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

        for k,v in target
            envstr = envstr + "\t%s %s \n" %(k.upper() , v)

        logpath = rg_log_path() + "/" + self.logpath;
        c = Template(content).substitute(SCRIPT=self.program, DAEMON=self.daemon,
                FOREVER=self.forever,LOG=logpath,UK=ukey,RUN_PATH=self.runpath,ENVS=envstr)
        _logger.info("zdemon conf:")
        _logger.info(c)
        if not os.path.exists(logpath) :
            rg_sh.shexec.execmd(" mkdir -p " + logpath)
        with  open(conf ,'w') as f :
            f.write(c)

class daemon (daemon_base,restag_unix):
    """
    示例:
    !R.daemon:
        script : "$${PRJ_ROOT}/src/apps/console/work.sh"
    """
    _script   = ""
    _daemon   = "True"
    _umask    = "022"
    _forever  = "True"
    _logpath  = "${PRJ_NAME}/"
    _runpath  = "${RUN_PATH}"
    _worker   = 1

class daemon_php(daemon_base,restag_unix):
    """
    示例:
    !R.daemon_php :
        script : "$${PRJ_ROOT}/src/apps/console/work.php"
        php_ini: "$${PRJ_ROOT}/conf/used/php.ini"
    """
    _php_ini  = "${PHP_INI}"
    _script   = ""
    _daemon   = "True"
    _umask    = "022"
    _forever  = "True"
    _logpath  = "${PRJ_NAME}/"
    _runpath  = "${RUN_PATH}"
    _worker   = 1

    def locate(self,context):
        daemon_base.locate(self,context)
        self.php_ini    = env_exp.value(self.php_ini)
        self.program    = "%s -c %s -f %s " %(get_env_conf().php,self.php_ini,self.script)
