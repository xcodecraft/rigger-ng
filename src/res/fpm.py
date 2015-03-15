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

class fpm_conf:
    def export_env2php(self):
        os_env_str = ''
        tmpfile    = value_of("${PRJ_ROOT}/run/") + self.prefix + '.env'
        for k,v in environ_items():
            if k == "SHELL" or k == '_':
                continue
            os_env_str += ( 'env[%s] = "%s"\n' %(k,v))
        if os.access(value_of("${PRJ_ROOT}/run/"), os.W_OK) :
            with open(tmpfile, 'w') as f: f.write (os_env_str)

    def export_monitorconf(self, conf_path, files_to_check):
        cmd    = "cd %s; %s/rigger restart -x %s" %(value_of('${PRJ_ROOT}'), rg_home() , self.__class__.__name__)
        prefix = os.path.dirname(conf_path)
        if not os.path.isdir(prefix):
           shexec.execmd("mkdir -p '%s'" % prefix)
        conf   = 'FILES=\\"%s\\";' % files_to_check.replace(',', ' ') + 'CMD=\\"%s\\"' % cmd
        shexec.execmd('echo "%s" > "%s"' %(conf, conf_path))

    def export_fpmconf(self):
        if not self.f_conf == self.fpm_conf:
            fpm_conf = 'online' if self.fpm_conf == 'online' else 'dev'
            run_user = env_exp.value("${USER}") if env_exp.value("${USER}") in [e.pw_name for e in pwd.getpwall()] else 'nobody' 
            cnt_min = str(int(self.fpm_cnt) - 10)
            cnt_max = str(int(self.fpm_cnt) + 10)
            conf_override = env_exp.value("\n".join(self.conf_override).replace(';' + fpm_conf, ''))
            tplpath = rg_home() + '/extension/res_conf/fpm_svc.conf.' + fpm_conf
            with open(tplpath,'r') as ftpl :
                tpl = ftpl.read()
                tpl = Template(tpl).substitute(POOL_NAME=self.prefix,USER=run_user,FPM_CNT=self.fpm_cnt,FPM_CNT_MIN=cnt_min,FPM_CNT_MAX=cnt_max,CONF_OVERRIDE=conf_override)
                tmp_path = value_of("${PRJ_ROOT}/run/" + self.f_conf.replace('/', '_'))
                with open(tmp_path, 'w') as f: f.write (tpl)
                shexec.execmd("mv '%s' '%s'" % (tmp_path, self.f_conf))

class fpm(interface.resource,fpm_conf):
    fpm_conf   = "dev" 
    fpm_cnt    = "20"
    sock_id    = ""
    php_ini    = "${PHP_INI}"
    php_fpm    = "/usr/local/php-5.3/sbin/php-fpm"

    conf_override = []
    sudo       = True 

    def _allow(self,context) :
        return True

    def _before(self,context):
        self.sudo       = value_of(self.sudo)
        #FIXME  
        #self.prefix     = value_of("rgapp-${USER}-${PRJ_KEY}-${_RG_SYS}" + self.sock_id)
        self.prefix     = value_of("rgapp-${USER}-${PRJ_KEY}" + self.sock_id)
        self.php_ini    = value_of(self.php_ini)
        self.fpm_conf   = value_of(self.fpm_conf)
        cur_path        = os.path.dirname(os.path.realpath(__file__))

        if os.path.isfile(self.fpm_conf):
            self.f_conf = self.fpm_conf
        elif self.fpm_conf == 'online' : 
            self.f_conf = value_of("${PRJ_ROOT}")  +  '/' + self.prefix + '/fpm_svc.conf.online'
        else : 
            self.f_conf = value_of("${PRJ_ROOT}") +  '/' + self.prefix + '/fpm_svc.conf.dev'

        cmdtpl="${PATH}/fpm_ctrl.sh -b ${FPM_BIN} -c ${FPM_CONF} -f ${PHP_INI} -p ${PREFIX} -r ${PRJ_ROOT} -n ${RUN_PATH}"
        self.base_cmd = Template(cmdtpl).substitute(
            PATH        =   cur_path,
            FPM_BIN     =   self.php_fpm,
            FPM_CONF    =   self.f_conf,
            PHP_INI     =   self.php_ini,
            PREFIX      =   self.prefix,
            PRJ_ROOT    =   value_of('${PRJ_ROOT}'),
            #RUN_PATH=rg_run_path() FIXME
            RUN_PATH=value_of("${PRJ_ROOT}")
            )

    def _config(self,context):
        prefix_dir = value_of("${PRJ_ROOT}") + '/' + self.prefix 
        if not os.path.isdir(prefix_dir):
           shexec.execmd("mkdir -p '%s'" % prefix_dir)
        self.export_monitorconf(prefix_dir  + '/config.fpm', 'fpm.pid,fpm.sock')
        self.export_env2php()
        self.export_fpmconf()
        cmd = self.base_cmd + " -d config"
        shexec.execmd(cmd)

    def _start(self,context):
        cmd = self.base_cmd + " -d start"
        shexec.execmd(cmd)

    def _stop(self,context):
        cmd = self.base_cmd + " -d stop"
        shexec.execmd(cmd)

    def _check(self,context):
        cmdtpl = "cat " +  value_of("${PRJ_ROOT}") +  '/'   + self.prefix + "/fpm.pid 2>/dev/null | xargs ps | grep fpm"
        cnt_cmd = Template(cmdtpl).substitute(FPM_CONF=self.f_conf)
        check_proc("PHP-FPM", cnt_cmd, '1')

    def _reload(self,context):
        cmd = self.base_cmd+" -d reload"
        shexec.execmd(cmd)

    def _clean(self,context):
        cmd = self.base_cmd+" -d clean"
        shexec.execmd(cmd)

    def _restart(self,context):
        cmd = self.base_cmd+" -d restart"
        shexec.execmd(cmd)

