#coding=utf-8
import logging
import interface
import time
import random

from utls.rg_io  import rgio,rg_logger
from utls.rg_var import value_of
from utls.rg_sh  import shexec
from impl.rg_utls  import *
#from impl.rg_res  import *
from string import *

def stop_service(name,pidfile,sudo=False):
    path=os.path.dirname(os.path.realpath(__file__))
    if sudo :
        cmdtpl=" sudo %s/stop_proc.sh %s %s " %(path,pidfile,name)
    else:
        cmdtpl=" %s/stop_proc.sh %s %s " %(path,pidfile,name)
    cmd = Template(cmdtpl).substitute(NAME=name,PID_FILE=pidfile)
    shexec.execmd(cmd)

class varnishd(interface.resource):
    """
    !R.varnishd
        port:       "80"
        http_ip:    "0.0.0.0"
        admin_port: "2000"
        admin_ip:   "127.0.0.1"
        mem:        "20M"
        vcl:        "${PRJ_ROOT}/conf/used/local_cache.vcl"
        name:       "local_proxy_${ENV}"
        extras:     "-w 100,1000,60"
    """

    port       = "80"
    http_ip    = "0.0.0.0"
    admin_port = "2000"
    admin_ip   = "127.0.0.1"
    mem        = "20M"
    vcl        = ""
    extras     = ""
    name       = "rigger"

    varnishd   = "/usr/local/sbin/varnish"
    varnishadm = "/usr/local/sbin/varnishadm"

    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.port       = value_of(self.port)
            self.admin_port = value_of(self.admin_port)
            self.admin_ip   = value_of(self.admin_ip)
            self.http_ip    = value_of(self.http_ip)
            self.mem        = value_of(self.mem)
            self.vcl        = value_of(self.vcl)
            self.extras     = value_of(self.extras)
            self.name       = value_of(self.name)
            self.pid        = value_of("${PRJ_ROOT}/varnishd_${PRJ_KEY}_" + self.port + ".pid")

    def _start(self,context):
        cmdtpl = "if ! test -s $PID ; then sudo $VARNISHD -f $VCL -s malloc,$MEM -T $ADMIN_IP:$ADMIN_PORT -a $HTTP_IP:$PORT -P$PID -n $NAME $EXTRAS ; fi"
        cmd = Template(cmdtpl).substitute(
                VARNISHD    =   self.varnishd,
                MEM         =   self.mem,
                PORT        =   self.port,
                VCL         =   self.vcl,
                ADMIN_PORT  =   self.admin_port,
                ADMIN_IP    =   self.admin_ip,
                HTTP_IP     =   self.http_ip,
                PID         =   self.pid,
                NAME        =   self.name,
                EXTRAS      =   self.extras
                )
        shexec.execmd(cmd)

    def _stop(self,context):
        if get_key("Are you sure stop Varnishd? (y/N)", context)  == "y" :
            stop_service("Varnished",self.pid, True)

    def _reload(self,context):
        confname = "vcl_%s_%d" %(time.strftime("%H_%M_%S",time.localtime()) , int(random.random() * 100 ) )
        cmdtpl = """ $VARNISHADM  -n $NAME vcl.load $CONFNAME $VCL ; $VARNISHADM  -n $NAME vcl.use $CONFNAME """;
        cmd = Template(cmdtpl).substitute(
                VARNISHADM  = self.varnishadm,
                VCL         = self.vcl,
                ADMIN_PORT  = self.admin_port ,
                NAME        = self.name,
                CONFNAME    = confname
                )
        shexec.execmd(cmd)

    def _check(self,context):
        cmdtpl = "$VARNISHADM -T localhost:$ADMIN_PORT  status ";
        vns_test = Template(cmdtpl).substitute(
                VARNISHADM  = self.varnishadm,
                ADMIN_PORT  = self.admin_port ,
                )
        cmd = " sudo rm -rf /tmp/varnish_ok  ; if  " +  vns_test + "  ; then  sudo  touch  /tmp/varnish_ok;  fi  "
        shexec.execmd(cmd)
        self._check_print(os.path.exists("/tmp/varnish_ok"),"varnishd")

