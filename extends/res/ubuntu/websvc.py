#coding=utf-8
import logging
import interface

from utls.rg_io  import rg_logger
from utls.rg_var import value_of
from utls.rg_sh  import shexec
from impl.rg_utls  import *
from res.base   import *
from utls.rg_sh  import shexec
from res_base.websvc import *


class nginx_conf(nginx_conf_base):
    """
    !R.nginx_conf
        tpl : "${PRJ_ROOT}/conf/options/nginx.conf"
    """

    name = "${PRJ_NAME}_${SYS_NAME}_${USER}.conf"
    src  = "${PRJ_ROOT}/conf/used/nginx.conf"
    tpl  = "${PRJ_ROOT}/conf/options/nginx.conf"
    dst  = "/etc/nginx/sites-enabled/"
    bin  = "/usr/sbin/service nginx"


