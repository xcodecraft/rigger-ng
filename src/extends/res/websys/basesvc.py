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
from daemon     import *
import utls.check

class beanstalkd_shared (daemon_base):
    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.worker     = 1
            self.ip         = res_utls.value(self.ip)
            self.binlog     = res_utls.value(self.binlog)
            self.port       = res_utls.value(str(self.port))
            self.beanstalkd = res_utls.value(self.beanstalkd)
            self.tag        = "beanstalk-%s" %self.port
            self.blog_path  = "%s/beanstalk-%s" %(self.binlog, self.port)
            self.script     = "%s -l %s -p%s -b %s " %(self.beanstalkd, self.ip,self.port,self.blog_path)
            daemon_base._before(self,context)
    def _config(self,context):
        cmdtpl ="if test ! -e $DST; then   mkdir -p $DST ; fi ;   chmod a+rw $DST; "
        cmd = Template(cmdtpl).substitute(DST=self.blog_path)
        self.execmd(cmd)
        daemon_base._config(self,context)

    def depend(self,m,context):
        m.check_exists(self.beanstalkd)


