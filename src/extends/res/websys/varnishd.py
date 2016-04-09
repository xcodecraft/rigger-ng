#coding=utf-8
import logging
import interface
import time
import random


from utls.rg_io  import rgio,rg_logger
from utls.rg_var import value_of
from utls.rg_sh  import shexec
# from impl.rg_utls  import *
from res.base   import *
from string import *
import impl.rg_utls


class varnishd_shared(interface.resource,res_utls):

    # svc_port   = "80"
    # svc_ip     = "0.0.0.0"
    # admin_port = "2000"
    # admin_ip   = "127.0.0.1"
    # mem        = "20M"
    # vcl        = ""
    # extras     = ""
    # name       = ""
    # varnishd   = "/usr/local/varnish/sbin/varnishd"
    # varnishadm = "/usr/local/varnish/bin/varnishadm"

    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.svc_port   = value_of(self.svc_port)
            self.admin_port = value_of(self.admin_port)
            self.admin_ip   = value_of(self.admin_ip)
            self.svc_ip     = value_of(self.svc_ip)
            self.mem        = value_of(self.mem)
            self.vcl        = value_of(self.vcl)
            self.extras     = value_of(self.extras)
            self.name       = value_of(self.name)
            self.pid        = value_of("${RUN_PATH}/varnishd_" + self.svc_port + ".pid")
            self.varnishd   = value_of(self.varnishd)
            self.varnishadm = value_of(self.varnishadm)

    def _start(self,context):
        cmdtpl = "if ! test -s $PID ; then sudo $VARNISHD -f $VCL -s malloc,$MEM -T $ADMIN_IP:$ADMIN_PORT -a $SVC_IP:$PORT -P$PID -n $NAME $EXTRAS ; fi"
        cmd = Template(cmdtpl).substitute(
                VARNISHD   = self.varnishd,
                MEM        = self.mem,
                PORT       = self.svc_port,
                VCL        = self.vcl,
                ADMIN_PORT = self.admin_port,
                ADMIN_IP   = self.admin_ip,
                SVC_IP     = self.svc_ip,
                PID        = self.pid,
                NAME       = self.name,
                EXTRAS     = self.extras
                )
        shexec.execmd(cmd)
        time.sleep(2)

    def _stop(self,context):
        if os.path.exists(self.pid) :
            # if impl.rg_utls.get_key("Are you sure stop Varnishd? (y/N)", context)  == "y" :
            cmdtpl = "cat $PID | xargs kill ; rm $PID  "
            cmd = Template(cmdtpl).substitute( PID = self.pid)
            shexec.execmd(cmd)

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
        # pass
        cmdtpl = "$VARNISHADM -n $NAME  status ";
        vns_test = Template(cmdtpl).substitute(
                VARNISHADM  = self.varnishadm,
                NAME        = self.name
                )
        # cmd = " sudo rm -rf /tmp/varnish_ok  ; if  " +  vns_test + "  ; then  sudo  touch  /tmp/varnish_ok;  fi  "
        cmd = vns_test
        shexec.execmd(cmd)
        # self._check_print(os.path.exists("/tmp/varnish_ok"),"varnishd")


