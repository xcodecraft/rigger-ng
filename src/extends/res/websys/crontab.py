#coding=utf-8
import logging
import interface
import time
import random

from utls.rg_io  import rgio,rg_logger
from utls.rg_var import value_of
from utls.rg_sh  import shexec,check_proc
from utls.sysconf import  sysconf
from impl.rg_utls import *
from string     import *
from res.base   import *
import utls.check


class crontab_base(interface.resource,res_utls):
    # key   = "NO1"
    # cron  = None
    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.cron     = res_utls.value(self.cron)
            self.key      = res_utls.value(self.key)
            user          = res_utls.value("${USER}")
            self.tmp_cron = context.run_path + "/" + self.key + ".cron"
            self.tag      = res_utls.value("${PRJ_NAME}-${SYS_NAME}-%s" %(self.key))
    def _start(self,context):
        self.append_conf(context)
    def _stop(self,context):
        self.clean_conf(context)
    def append_conf(self,context):
        if not os.path.exists(self.cron):
            raise interface.rigger_exception("cron file not exists : %s" %self.cron)
        # import pdb
        # pdb.set_trace() ;

        self.execmd("/usr/bin/crontab -l > %s " %(self.tmp_cron) ,okcode=[0,256])
        conf    = sysconf(self.tmp_cron,"#")
        newcron = conf.replace_by_file(self.tag,self.cron)
        self.execmd("crontab  %s " %(newcron))

    def clean_conf(self,context):
        self.execmd("/usr/bin/crontab -l > %s " %(self.tmp_cron) ,okcode=[0,256])
        conf    = sysconf(self.tmp_cron,"#")
        newcron = conf.clean(self.tag)
        self.execmd("/usr/bin/crontab  %s " %(newcron))


