#coding=utf-8
import logging
import interface
import time
import random
from shared.fpm import *
from shared.daemon import *
from shared.basesvc import *

class fpm_pool(fpm_pool_base):
    bin  = "/sbin/service php5-fpm"
    src  = "${PRJ_ROOT}/conf/used/fpm.conf"
    dst  = "/etc/php5/fpm/pool.d/${PRJ_NAME}_${SYS_NAME}.conf"
    tpl  = "${PRJ_ROOT}/conf/options/fpm.conf"

class fpm(fpm_base):
    tag      = ""
    bin      = "/usr/local/php/sbin/php-fpm"
    ini      = "${PRJ_ROOT}/conf/used/${SYS_NAME}_php.ini"
    ini_tpl  = "${PRJ_ROOT}/conf/options/fpm.ini"
    conf     = "${PRJ_ROOT}/conf/used/${SYS_NAME}_fpm.conf"
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
    bin  = "/sbin/service nginx"

from shared.mysql import *
class mysql(mysql_base):

    """
    !R.mysql:
        host: "127.0.0.1"
        sql: "init.sql"
    """
    host     = "localhost"
    name     = ""
    user     = ""
    password = ""
    sql      = ""
    bin        = "/usr/local/mysql/bin/mysql"

class daemon(daemon_base):
    """
    示例:
    !R.daemon:
        script : "$${PRJ_ROOT}/src/apps/console/work.sh"
    """
    script   = ""
    daemon   = "True"
    umask    = "022"
    forever  = "True"
    logpath  = "${RUN_PATH}"
    confpath = "${PRJ_ROOT}/conf/used"
    runpath  = "${RUN_PATH}"
    worker   = 1
    tag      = ""
    zdaemon  = "/usr/local/python/bin/zdaemon"

class daemon_php(daemon_base_php):
    """
    示例:
    !R.daemon_php :
        script : "$${PRJ_ROOT}/src/apps/console/work.php"
        php_ini: "$${PRJ_ROOT}/conf/used/php.ini"
    """
    confpath = "${PRJ_ROOT}/conf/used"
    php_ini  = "${PHP_INI}"
    php_bin  = "${PHP_BIN}"
    script   = ""
    daemon   = "True"
    umask    = "022"
    forever  = "True"
    logpath  = "${RUN_PATH}"
    runpath  = "${RUN_PATH}"
    zdaemon  = "/usr/local/python/bin/zdaemon"
    worker   = 1
    tag      = ""

class beanstalkd (beanstalkd_shared):
    port       = "11300"
    ip         = "0.0.0.0"
    verbosity  = False
    daemon     = "True"
    umask      = "022"
    forever    = "True"
    logpath    = "${RUN_PATH}/"
    binlog     = "/data/${PRJ_NAME}"
    runpath    = "${RUN_PATH}"
    beanstalkd = "/usr/local/beanstalkd/bin/beanstalkd"
    zdaemon    = "/usr/local/python/bin/zdaemon"
    confpath   = "${PRJ_ROOT}/conf/used"

