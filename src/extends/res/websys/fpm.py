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
from websys.shared_utls import *
import utls.check


class fpm_pool_base(interface.control_box,interface.base):
    # bin  = "/usr/sbin/service php5-fpm"
    # src  = "${PRJ_ROOT}/conf/used/fpm.conf"
    # dst  = "/etc/php5/fpm/pool.d/${PRJ_NAME}_${SYS_NAME}.conf"
    # tpl  = "${PRJ_ROOT}/conf/options/fpm.conf"

    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.bin  = res_utls.value(self.bin)
            self.name = res_utls.value(self.name)
            self.dst  = res_utls.value(self.dst)
            self.src  = res_utls.value(self.src)
            self.src  = tpldst_path(self.tpl,self.src)
            self.tpl  = res_utls.value(self.tpl)

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

            sc            = service_ctrol(self.bin)
            sc.sudo       = self.sudo
            self.append(sc)
            interface.control_box._before(self,context)

    def _check(self,context):
        self._check_print(os.path.exists(self.dst),self.dst)


class fpm_ctrl(interface.resource,res_utls):
    bin  = ""
    tag  = ""
    ini  = ""
    conf = ""
    args = ""
    """
    pid: ${RUN_PATH}/fpm_${tag}.pid
    env: ${RUN_PATH}/fpm_${tag}.env
    """

    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.bin  = res_utls.value(self.bin)
            self.tag  = res_utls.value(self.tag)
            self.ini  = res_utls.value(self.ini)
            self.conf = res_utls.value(self.conf)
            self.args = res_utls.value(self.args)
            self.env  = res_utls.value("${RUN_PATH}/fpm_%s.env" %self.tag)
            self.pid  = res_utls.value("${RUN_PATH}/fpm_%s.pid" %self.tag)

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
        # tpl = "$BIN -c $INI -g $PID -y $CONF $args"
        tpl = "$BIN  --pid $PID -c $INI --fpm-config $CONF $args"
        cmd = Template(tpl).substitute(
                BIN   = self.bin,
                INI   = self.ini,
                PID   = self.pid,
                CONF  = self.conf,
                args  = self.args
                )
        self.execmd(cmd)
    def _stop(self,context) :
        cmd = " if test -e %s ; then  kill -QUIT `cat %s` ; fi  " %(self.pid,self.pid )
        self.execmd(cmd)
    def _reload(self,context) :
        cmd = " if test -e %s ; then  kill -USR2  `cat %s` ; fi  " %(self.pid,self.pid )
        self.execmd(cmd)




class fpm_base(interface.control_box,interface.base):
    # tag      = ""
    # bin      = "/usr/sbin/php5-fpm"
    # ini      = "${PRJ_ROOT}/conf/used/${SYS_NAME}.fpm.ini"
    # ini_tpl  = "${PRJ_ROOT}/conf/options/fpm.ini"
    # conf     = "${PRJ_ROOT}/conf/used/${SYS_NAME}.fpm.conf"
    # conf_tpl = "${PRJ_ROOT}/conf/options/fpm.conf"
    # args     = "-D"

    def _before(self,context):
        with res_context(self.__class__.__name__) :
            tpl_ini       = res.file_tpl()
            tpl_ini.sudo  = self.sudo
            tpl_ini.tpl   = res_utls.value(self.ini_tpl)
            tpl_ini.dst   = res_utls.value(self.ini)
            self.append(tpl_ini)

            tpl_conf      = res.file_tpl()
            tpl_conf.sudo = self.sudo
            tpl_conf.tpl  = res_utls.value(self.conf_tpl)
            tpl_conf.dst  = res_utls.value(self.conf)
            self.append(tpl_conf)

            ctrl          = fpm_ctrl()
            ctrl.sudo     = self.sudo
            ctrl.tag      = res_utls.value(self.tag)
            ctrl.ini      = res_utls.value(self.ini)
            ctrl.conf     = res_utls.value(self.conf)
            ctrl.args     = res_utls.value(self.args)
            ctrl.bin      = res_utls.value(self.bin)

            self.append(ctrl)
            interface.control_box._before(self,context)

