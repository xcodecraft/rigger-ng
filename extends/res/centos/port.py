import logging
import interface
import time
import random
from shared.fpm import *

class fpm_pool(fpm_pool_base):
    bin  = "/usr/sbin/service php5-fpm"
    src  = "${PRJ_ROOT}/conf/used/fpm.conf"
    dst  = "/etc/php5/fpm/pool.d/${PRJ_NAME}_${SYS_NAME}.conf"
    tpl  = "${PRJ_ROOT}/conf/options/fpm.conf"

class fpm(fpm_base):
    tag      = ""
    bin      = "/usr/local/php-5.3/sbin/php-fpm"
    ini      = "${PRJ_ROOT}/conf/used/${SYS_NAME}.fpm.ini"
    ini_tpl  = "${PRJ_ROOT}/conf/options/fpm.ini"
    conf     = "${PRJ_ROOT}/conf/used/${SYS_NAME}.fpm.conf"
    conf_tpl = "${PRJ_ROOT}/conf/options/fpm.conf"
    args     = ""

from shared.websvc import *

class nginx_conf(nginx_conf_base):
    """
    !R.nginx_conf
        tpl : "${PRJ_ROOT}/conf/options/nginx.conf"
    """

    name = "${PRJ_NAME}_${SYS_NAME}_${USER}.conf"
    src  = "${PRJ_ROOT}/conf/used/nginx.conf"
    tpl  = "${PRJ_ROOT}/conf/options/nginx.conf"
    dst  = "/usr/local/nginx/conf/include/"
    bin  = "/usr/sbin/service nginx"

from shared.mysql import *
class mysql(mysql_base):
    """
    !R.mysql:
        host: "127.0.0.1"
        init: "init.sql"
    """
    bin        = "/usr/bin/mysql"
