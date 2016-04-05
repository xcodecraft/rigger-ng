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

# def stop_service(name,pidfile,sudo=False):
#     path=os.path.dirname(os.path.realpath(__file__))
#     if sudo :
#         cmdtpl=" sudo %s/stop_proc.sh %s %s " %(path,pidfile,name)
#     else:
#         cmdtpl=" %s/stop_proc.sh %s %s " %(path,pidfile,name)
#     cmd = Template(cmdtpl).substitute(NAME=name,PID_FILE=pidfile)
#     shexec.execmd(cmd)
#
# class varnishd(resource,restag_svc):
#     """
#     """
#     port       = "80"
#     http_ip    = "0.0.0.0"
#     admin_port = "2000"
#     admin_ip   = "127.0.0.1"
#     mem        = "20M"
#     vcl        = ""
#     extras     = ""
#     runpath    = "${RUN_PATH}"
#     name       = "rigger"
#     varnishd   = "/usr/local/varnish/sbin/varnishd"
#     def _before(self,context):
#         self.port       = res_utls.value(self.port)
#         self.admin_port = res_utls.value(self.admin_port)
#         self.admin_ip   = res_utls.value(self.admin_ip)
#         self.http_ip    = res_utls.value(self.http_ip)
#         self.mem        = res_utls.value(self.mem)
#         self.vcl        = res_utls.value(self.vcl)
#         extras          = res_utls.value(self.extras)
#         self.name       = res_utls.value(self.name)
#         self.runpath    = res_utls.value(self.runpath)
#         self.pid        = self.runpath  + "/varnishd_" + "_" + self.port + ".pid"
#
#     def _start(self,context):
#         cmdtpl="if ! test -s $PID ; then sudo $VARNISHD -f $VCL -s malloc,$MEM -T $ADMIN_IP:$ADMIN_PORT -a $HTTP_IP:$PORT -P$PID -n $NAME $EXTRAS ; fi"
#         cmd = Template(cmdtpl).substitute( VARNISHD=get_env_conf().varnishd,
#                 MEM         =   self.mem,PORT= self.port,
#                 VCL         =   self.vcl,
#                 ADMIN_PORT  =   self.admin_port ,
#                 ADMIN_IP    =   self.admin_ip   ,
#                 HTTP_IP     =   self.http_ip,
#                 PID         =   self.pid,
#                 NAME        =   self.name,
#                 EXTRAS      =   self.extras
#                 )
#         rg_sh.shexec.execmd(cmd)
#     def _stop(self,context):
#          stop_service("Varnished",self.pid, True)
#     def _reload(self,context):
#         confname = "vcl_%s_%d" %(time.strftime("%H_%M_%S",time.localtime()) , int(random.random() * 100 ) )
#         cmdtpl = """ $VARNISHADM  -n $NAME vcl.load $CONFNAME $VCL ; $VARNISHADM  -n $NAME vcl.use $CONFNAME """;
#         cmd = Template(cmdtpl).substitute( VARNISHADM=get_env_conf().varnishadm,
#                 VCL         = self.vcl,
#                 ADMIN_PORT  = self.admin_port ,
#                 NAME        = self.name,
#                 CONFNAME=confname
#                 )
#         rg_sh.shexec.execmd(cmd)
#     def _check(self,context):
#         cmdtpl = "$VARNISHADM -T localhost:$ADMIN_PORT  status ";
#         vns_test = Template(cmdtpl).substitute( VARNISHADM=get_env_conf().varnishadm, ADMIN_PORT=self.admin_port )
#         cmd = " sudo rm -rf /tmp/varnish_ok  ; if  " +  vns_test + "  ; then  sudo  touch  /tmp/varnish_ok;  fi  "
#         self.execmd(cmd)
#         self.check_print(os.path.exists("/tmp/varnish_ok"),"varnishd")
#
#
# class local_proxy(resource,restag_extsvc):
#     """local_proxy service
#        ä½¿ç¨å nginx
#     """
#     _path = ""
#     def locate(self,context):
#         self.path = res_utls.value(self.path)
#     def start(self,context):
#         self.reload(context)
#     def stop(self,context):
#         pass
#     def reload(self,context):
#         lproxy = get_env_conf().local_proxy
#         if len(self.path ) > 0 :
#             lproxy  = self.path
#         if not os.path.exists(lproxy):
#             raise error.rigger_exception("local_proxy service not found: %s" %lproxy)
#         path=os.path.dirname(os.path.realpath(__file__ + "../../"))
#         path=os.path.dirname(path)
#         cmd = "cd %s ; %s/rigger reload -s cache " %(lproxy,path)
#         rg_sh.shexec.execmd(cmd)
#     def check(self,context):
#         pass
#     def depend(self,m,context):
#         m.check_exists(get_env_conf().varnishadm)
#
# class local_proxy_conf( file_tpl,restag_extsvc):
#     """
#     """
#     _link = "/etc/local_proxy/sys"
#     _mod    = "a+w"
#     def locate(self,context):
#         file_tpl.locate(self,context)
#         self.link =  res_utls.value(self.link)
#     def config(self,context):
#         file_tpl.config(self,context)
#         tpl =  'if test  -L $PATH/$DST ; then rm $PATH/$DST ; fi; ln -s $SRC $PATH/$DST'
#         cmd = Template(tpl).substitute(PATH=self.link, DST=os.path.basename(self.dst), SRC=self.dst)
#         rg_sh.shexec.execmd(cmd)
#     def clean(self,context):
#         tpl =  'if test -L $PATH/$DST ; then rm $PATH/$DST ; fi ; if test -e $SRC ; then  rm  $SRC; fi ;'
#         cmd = Template(tpl).substitute(PATH=self.link, DST=os.path.basename(self.dst), SRC=self.dst)
#         rg_sh.shexec.execmd(cmd)
#
#     def depend(self,m,context):
#         m.check_exists(self.link)
