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


class hosts_base(interface.resource,res_utls):
    # hosts  = None
    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.hosts     = res_utls.value(self.hosts)
            user           = res_utls.value("${USER}")
            self.tmp_hosts = context.run_path + "/tmp.hosts"
            self.tag       = res_utls.value("${PRJ_NAME}-${SYS_NAME}")
    def _config(self,context):
        self.append_conf(context)
    def _clean(self,context):
        self.clean_conf(context)
    def append_conf(self,context):
        if not os.path.exists(self.hosts):
            raise interface.rigger_exception("hosts file not exists : %s" %self.hosts)
        # import pdb
        # pdb.set_trace() ;

        self.execmd("cat /etc/hosts > %s " %(self.tmp_hosts) ,okcode=[0,256])
        conf    = sysconf(self.tmp_hosts,"#")
        newhosts = conf.replace_by_file(self.tag,self.hosts)
        self.execmd("cat %s > /etc/hosts" %(newhosts))

    def clean_conf(self,context):
        tmp_hosts =  "/tmp/" + self.tmp_hosts.replace('/','_') ;
        self.execmd("cat /etc/hosts > %s " %(tmp_hosts) ,okcode=[0,256])
        conf    = sysconf(tmp_hosts,"#")
        newhosts = conf.clean(self.tag)
        self.execmd("cat %s > /etc/hosts  ; rm %s" %(newhosts, tmp_hosts))


