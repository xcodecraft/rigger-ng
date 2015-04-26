#coding=utf-8
import logging
import interface
import time
import random

from utls.rg_io  import rg_logger
from utls.rg_var import value_of
from utls.rg_sh  import shexec
from impl.rg_utls  import *
from string import *
from res.base import *
import utls.check


class fpm_pool(interface.control_box,interface.base):
    name = "${PRJ_NAME}_${SYS_NAME}.conf"
    src  = "${PRJ_ROOT}/conf/used/fpm.conf"
    tpl  = "${PRJ_ROOT}/conf/options/fpm.conf"

    def _before(self,context):
        self.name     = res_utls.value(self.name)
        self.dst      = res_utls.value(os.path.join(context.php_def.fpm_conf_root,self.name) )
        self.src      = res_utls.value(self.src)
        self.tpl      = res_utls.value(self.tpl)

        tpl_res       = res.file_tpl()
        tpl_res.sudo  = self.sudo
        tpl_res.tpl   = self.tpl
        tpl_res.dst   = self.src
        self.append(tpl_res)

        link_res      = res.link()
        link_res.sudo = self.sudo
        link_res.dst  = self.dst
        link_res.src  = self.src
        self.append(link_res)

        sc            = service_ctrol("php5-fpm")
        sc.sudo       = self.sudo
        self.append(sc)
        interface.control_box._before(self,context)

    def _check(self,context):
        self._check_print(os.path.exists(self.dst),self.dst)


class fpm_ctrl(interface.resource,res_utls):
    prefix = ""
    ini    = ""
    conf   = ""
    extra  = "-D"
    """
    pid: ${RUN_PATH}/fpm_${PREFIX}.pid
    env: ${RUN_PATH}/fpm_${PREFIX}.env
    """

    def _before(self,context):
        self.bin    = "/usr/sbin/php5-fpm"
        self.prefix = res_utls.value(self.prefix)
        self.ini    = res_utls.value(self.ini)
        self.conf   = res_utls.value(self.conf)
        self.extra  = res_utls.value(self.extra)
        self.env    = res_utls.value("${RUN_PATH}/fpm_%s.env" %self.prefix)
        self.pid    = res_utls.value("${RUN_PATH}/fpm_%s.pid" %self.prefix)

    def _config(self,context):
        self.export_env(context)

    def export_env(self,context) :
        target= dict()
        utls.rg_var.export2dict(target)
        with   open(self.env,'w') as efile :
            for  k ,v in target.items() :
                v = res_utls.value(v)
                efile.write( "env[%s] = %s \n" %(k,v))

    def _start(self,context) :
        if os.path.exists(self.pid) :
            return
        # tpl = "$BIN -c $INI -g $PID -y $CONF $EXTRA"
        tpl = "$BIN  --pid $PID --fpm-config $CONF $EXTRA"
        cmd = Template(tpl).substitute(
                BIN   = self.bin,
                INI   = self.ini,
                PID   = self.pid,
                CONF  = self.conf,
                EXTRA = self.extra
                )
        self.execmd(cmd)
    def _stop(self,context) :
        cmd = " if test -e %s ; then  kill -QUIT `cat %s` ; fi  " %(self.pid,self.pid )
        self.execmd(cmd)
    def _reload(self,context) :
        cmd = " if test -e %s ; then  kill -USR2  `cat %s` ; fi  " %(self.pid,self.pid )
        self.execmd(cmd)




class fpm(interface.control_box,interface.base):
    prefix   = ""
    ini      = "${PRJ_ROOT}/conf/used/${SYS_NAME}.fpm.ini"
    ini_tpl  = "${PRJ_ROOT}/conf/options/fpm.ini"
    conf     = "${PRJ_ROOT}/conf/used/${SYS_NAME}.fpm.conf"
    conf_tpl = "${PRJ_ROOT}/conf/options/fpm.conf"
    # socket   = "${RUN_PATH}/${SYS_NAME}.socket"

    def _before(self,context):

        tpl_ini       = res.file_tpl()
        tpl_ini.sudo  = self.sudo
        tpl_ini.tpl   = res_utls.value(self.ini_tpl)
        tpl_ini.dst   = res_utls.value(self.ini)
        self.append(tpl_ini)

        tpl_conf       = res.file_tpl()
        tpl_conf.sudo  = self.sudo
        tpl_conf.tpl   = res_utls.value(self.conf_tpl)
        tpl_conf.dst   = res_utls.value(self.conf)
        self.append(tpl_conf)

        ctrl        = fpm_ctrl()
        ctrl.sudo   = self.sudo
        ctrl.prefix = self.prefix
        ctrl.ini    = self.ini
        ctrl.conf   = self.conf

        self.append(ctrl)
        interface.control_box._before(self,context)

