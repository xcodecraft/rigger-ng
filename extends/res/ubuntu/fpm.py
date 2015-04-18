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
    tpl  = "${PRJ_ROOT}/conf/option/fpm.conf"

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

