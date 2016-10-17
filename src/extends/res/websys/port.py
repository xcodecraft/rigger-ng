#coding=utf-8
import logging
import interface
import time
import random
from websys.fpm import *
from websys.daemon import *
from websys.basesvc import *
from websys.crontab import *
from websys.varnishd import *
from websys.hosts   import *

# class fpm_pool(fpm_pool_base):
#     bin  = "/sbin/service php5-fpm"
#     src  = "${PRJ_ROOT}/conf/used/fpm.conf"
#     dst  = "/etc/php5/fpm/pool.d/${PRJ_NAME}_${SYS_NAME}.conf"
#     tpl  = "${PRJ_ROOT}/conf/options/fpm.conf"

class fpm(fpm_base):
    tag      = ""
    bin      = "${PHP_FPM}"
    ini      = "${PRJ_ROOT}/conf/used/${SYS_NAME}_php.ini"
    ini_tpl  = "${PRJ_ROOT}/conf/options/fpm.ini"
    conf     = "${PRJ_ROOT}/conf/used/${SYS_NAME}_fpm.conf"
    conf_tpl = "${PRJ_ROOT}/conf/options/fpm.conf"
    args     = ""

from websys.websvc import *

class nginx_conf(nginx_conf_base):
    """
    !R.nginx_conf
        tpl : "${PRJ_ROOT}/conf/options/nginx.conf"
    """

    name    = "${PRJ_NAME}_${SYS_NAME}_${USER}.conf"
    src     = "${PRJ_ROOT}/conf/used/nginx.conf"
    tpl     = "${PRJ_ROOT}/conf/options/nginx.conf"
    dst     = "${NGINX_CONF}"
    bin     = "${NGINX_BIN}"
    testbin = "${NGINX_TESTBIN}"

from websys.mysql import *
class mysql(mysql_base):

    """
    !R.mysql
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
    !R.daemon
        script : "${PRJ_ROOT}/src/apps/console/work.sh"
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
    zdaemon  = "${ZDAEMON}"

class daemon_php(daemon_base_php):
    """
    示例:
    !R.daemon_php
        script : "${PRJ_ROOT}/src/apps/console/work.php"
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
    zdaemon  = "${ZDAEMON}"
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
    beanstalkd = "${BEANSTALKD}"
    zdaemon  = "${ZDAEMON}"
    confpath   = "${PRJ_ROOT}/conf/used"

class varnishd (varnishd_shared) :
    svc_port   = "80"
    svc_ip     = "0.0.0.0"
    admin_port = "2000"
    admin_ip   = "127.0.0.1"
    mem        = "20M"
    vcl        = ""
    extras     = ""
    name       = ""
    varnishd   = "${VARNISHD}"
    varnishadm = "${VARNISHADM}"

class crontab (crontab_base) :
    """
    !R.crontab
        cron : "${PRJ_ROOT}/conf/used/example.cron"
    """
    key   = "NO1"
    cron  = None

class hosts (hosts_base) :
    """
    !R.hosts
        hosts : "${PRJ_ROOT}/conf/used/example.hosts"
    """
    hosts  = None
