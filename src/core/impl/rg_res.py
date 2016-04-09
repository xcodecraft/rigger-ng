#coding=utf-8
# from string     import Template
# from setting    import *
#
# from interface.rg_def import resource
# from utls.rg_io import  rg_logger
# from res.files import file_tpl
# from utls import pattern
#
#
# class svctag:
#     pass
#
# class filetag:
#     pass
# class extag:
#     pass
# class pylontag:
#     pass
#
# class rgtag:
#     pass
#
#
#
# class controlor(resource):
#     def start(self,context):
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_start(r,context)
#
#     def stop(self,context):
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_stop(r,context)
#
#     def config(self,context):
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_config(r,context)
#
#     def depend_check(self,context):
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_depend(r,context)
#
#     def depend_ensure(self,context):
# #     这时子资源 locate 都没有执行   
#         pass
#     def locate(self,context):
#         if not self.obj_has('res'):
#             self.res = []
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_locate(r,context)
#     def data(self,context):
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_data(r,context)
#     def check(self,context):
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_check(r,context)
#
#     def reload(self,context):
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_reload(r,context)
#     def clean(self,context):
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_clean(r,context)
#     def shell(self,context):
#         if self.allow():
#             for r in self.res :
#                 r.set_parent( self.respath())
#                 call_shell(r,context)
#     def allow(self):
#         return True
#     def append(self,item):
#         self.res.append(item)
#     def push(self,item):
#         self.res.insert(0,item)
#
#
# class nginx (resource,svctag):
#     """support nginx"""
#     _need_reload = True
#     def local(self):
#         self.need_reload = env_exp.value(self.need_reload)
#
#     def start(self):
#         self.reload()
#     def stop(self):
#         pass
#     def reload(self):
#         if self.need_reload  :
#             cmd = get_env_conf().nginx_ctrl + ' reload '
#             shexec.execmd(cmd)
#     def check(self):
#         cmd = "ps auxww | grep nginx   "
#         check_proc("Nginx",cmd)
#         ngx_test = get_env_conf().nginx_ctrl.replace(" -s","")
#         ngx_test += " -t "
#         cmd = " sudo rm -rf /tmp/nginx_ok  ; if  " +  ngx_test + "  ; then  sudo  touch  /tmp/nginx_ok ;  fi  "
#         shexec.execmd(cmd)
#         self.check_print(os.path.exists("/tmp/nginx_ok"),"nginx conf")
#
# class local_proxy(resource,svctag):
#     """local_proxy service
#        使用同 nginx
#     """
#     _path = ""
#     def locate(self):
#         self.path = env_exp.value(self.path)
#     def start(self):
#         self.reload()
#     def stop(self):
#         pass
#     def reload(self):
#         lproxy = get_env_conf().local_proxy
#         if len(self.path ) > 0 :
#             lproxy  = self.path
#         if not os.path.exists(lproxy):
#             raise rigger_exception("local_proxy serive not found: %s" %lproxy)
#         path=os.path.dirname(os.path.realpath(__file__ + "../../"))
#         cmd = "cd %s ; %s/rigger reload -s cache " %(lproxy,path)
#         shexec.execmd(cmd)
#     def check(self):
#         pass
#
#
# #class file_tpl(resource,conf):
#
#
# class tpl(resource,filetag):
#     _dst = ""
#     _tpl = ""
#     def locate(self):
#         self.dst  = env_exp.value(self.dst)
#         self.tpl  = env_exp.value(self.tpl)
#
#     def config(self):
#         import tplngin
#         tplngin.tplworker().execute(self.tpl,self.dst)
#     def check(self):
#         self.check_print(os.path.exists(self.dst),self.dst)
#     def clean(self):
#         cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi "
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         shexec.execmd(cmd)
#     def info(self):
#         return self.dst
#
#
# class nginx_conf_tpl( file_tpl,svctag ):
#     _mod    = "a+w"
#     def config(self):
#         file_tpl.config(self)
#         dst_path  = get_env_conf().nginx_conf_path
#         tpl =  'if test  -L $PATH/$DST ; then rm $PATH/$DST ; fi; ln -s $SRC $PATH/$DST'
#         cmd = Template(tpl).substitute(PATH=dst_path, DST=os.path.basename(self.dst), SRC=self.dst)
#         shexec.execmd(cmd)
#     def clean(self):
#         dst_path  = get_env_conf().nginx_conf_path
#         tpl =  'if test -L $PATH/$DST ; then rm $PATH/$DST ; fi ; if test -e $SRC ; then  rm  $SRC; fi ;'
#         cmd = Template(tpl).substitute(PATH=dst_path, DST=os.path.basename(self.dst), SRC=self.dst)
#         shexec.execmd(cmd)
#
# class local_proxy_conf( file_tpl,svctag ):
#     """
#         使用同 nginx_conf_tpl
#     """
#     _link = "/etc/local_proxy/sys"
#     _mod    = "a+w"
#     def locate(self):
#         file_tpl.locate(self)
#         self.link =  env_exp.value(self.link)
#     def config(self):
#         file_tpl.config(self)
#         tpl =  'if test  -L $PATH/$DST ; then rm $PATH/$DST ; fi; ln -s $SRC $PATH/$DST'
#         cmd = Template(tpl).substitute(PATH=self.link, DST=os.path.basename(self.dst), SRC=self.dst)
#         shexec.execmd(cmd)
#     def clean(self):
#         link_path  = "/etc/local_proxy/sys"
#         tpl =  'if test -L $PATH/$DST ; then rm $PATH/$DST ; fi ; if test -e $SRC ; then  rm  $SRC; fi ;'
#         cmd = Template(tpl).substitute(PATH=self.link, DST=os.path.basename(self.dst), SRC=self.dst)
#         shexec.execmd(cmd)
#
# class apache_conf_tpl( file_tpl,svctag ):
#     _mod    = "a+w"
#     def config(self):
#         file_tpl.config(self)
#         dst_path  = get_env_conf().apache_conf_path
#         tpl =  'if test -L $PATH/$DST ; then rm $PATH/$DST ; fi ;ln -s $SRC $PATH/$DST'
#         cmd = Template(tpl).substitute(PATH=dst_path, DST=os.path.basename(self.dst), SRC=self.dst)
#         shexec.execmd(cmd)
#     def clean(self):
#         dst_path  = get_env_conf().apache_conf_path
#         tpl =  'if test -L $PATH/$DST ; then  rm $PATH/$DST ; fi; if test -e $SRC ; then rm $SRC ; fi;'
#         cmd = Template(tpl).substitute(PATH=dst_path, DST=os.path.basename(self.dst), SRC=self.dst)
#         shexec.execmd(cmd)
#
#
# class logrotate( file_tpl ,svctag):
#     _mod    = "a+w"
#     def config(self):
#         file_tpl.config(self)
#         dst_path  = get_env_conf().logrotate
#         tpl =  'if test -e $PATH/$DST ; then rm $PATH/$DST ; fi ;ln -s $SRC $PATH/$DST'
#         cmd = Template(tpl).substitute(PATH=dst_path, DST=os.path.basename(self.dst), SRC=self.dst)
#         shexec.execmd(cmd)
#     def clean(self):
#         dst_path  = get_env_conf().logrotate
#         tpl =  'if test -e $PATH/$DST ; then  rm $PATH/$DST ; fi; if test -e $SRC ; then rm $SRC ; fi;'
#         cmd = Template(tpl).substitute(PATH=dst_path, DST=os.path.basename(self.dst), SRC=self.dst)
#         shexec.execmd(cmd)
#
# class apache (resource,svctag):
#     def start(self):
#         self.reload()
#     def stop(self):
#         pass;
#     def reload(self):
#         cmd = get_env_conf().apache_ctrl + ' graceful'
#         shexec.execmd(cmd)
#
#     def check(self):
#         cmd = "ps auxww | grep httpd "
#         check_proc("Apache",cmd)
#
#
# #class files (resource):
# #    pass
#
#
# class shell(resource,extag):
#     """execute shell script in conf file"""
#     _script = ""
#     def exec_script(self,args):
#         if os.path.exists(self.script) :
#             cmd = self.script  +  " " + args
#             shexec.execmd(cmd,True)
#
#     def locate(self):
# #        if  not self.env is None:
# #            self.env.locate()
#         self.script = env_exp.value(self.script)
#
#     def config(self):
#         self.exec_script("config")
#
#     def start(self):
#         self.exec_script("start")
#
#     def stop(self):
#         self.exec_script("stop")
#     def data(self):
#         self.exec_script("data")
#     def shell(self):
#         self.exec_script("shell")
#     def reload(self):
#         self.exec_script("reload")
#
#     def clean(self):
#         self.exec_script("clean")
#     def check(self):
#         exists = os.path.exists(self.script)
#         self.check_print(exists,self.script)
#         self.exec_script("check")
#
#     def info(self):
#         return self.script
#
# class console_php(resource,extag):
#     def locate(self):
# #        if  not self.env is None:
# #            self.env.locate()
#         self.script = env_exp.value(self.script)
#
#     def config(self):
#         cmd = self.script  +  " config"
#         self.shell(cmd)
#
#     def start(self):
#         cmd = self.script  +  " start"
#         self.shell(cmd)
#
#     def stop(self):
#         cmd = self.script  +  " stop"
#         self.shell(cmd)
#     def data(self):
#         cmd = self.script  +  " data"
#         self.shell(cmd)
#     def shell(self):
#         cmd = self.script  +  " shell"
#         self.shell(cmd)
#     def reload(self):
#         cmd = self.script  +  " reload"
#         self.shell(cmd)
#
#     def clean(self):
#         cmd = self.script  +  " clean"
#         self.shell(cmd)
#
#     def check(self):
#         exists = os.path.exists(self.script)
#         self.check_print(exists,self.script)
#         if exists :
#             cmd = self.script  +  " check"
#             self.shell(cmd)
#
#     def shell(self,script):
#         php = get_env_conf().php
#         ini = env_exp.value("${PHP_INI}")
#         cmd = php + "  -c " + ini + " "  +  script
#         shexec.execmd(cmd)
#
# class dx_shell(resource):
#     def __init__(self,env,script):
# #        self.env = env
#         self.script = script
#     def locate(self):
# #        self.env.locate()
#         self.script = env_exp.value(self.script)
#     def shell(self):
#         cmd = self.script
#         shexec.execmd(cmd)
#
#
# class phpunit(resource,pattern.singleton):
#     _ini        = "${PHP_INI}"
#     _suffix     = "test.php"
#     _path       = ""
#     _conf       = ""
#     def __init__(self,script=""):
#         self.path = ""
#         self.conf = ""
#         if re.match(r'.+\.xml$',script):
#             self.conf = script
#         else:
#             self.path = script
#
#     def locate(self):
#         self.path = env_exp.value(self.path)
#         self.conf = env_exp.value(self.conf)
#         self.ini  = env_exp.value(self.ini)
#         self.run_path = env_exp.value("${PRJ_ROOT}")
#         self.xml_conf = self.run_path + "/run/phpunit.xml"
#
#     def build_conf(self):
#         content = """
# <phpunit>
#     <testsuites>
#         <testsuite name="phpunit auto conf ">
#             <directory suffix="$SUFFIX">$PATH</directory>
#         </testsuite>
#     </testsuites>
# </phpunit>
# """
#         if os.path.isabs(self.path):
#             path = self.path
#         else:
#             path = self.run_path + "/" + self.path
#
#         c = Template(content).substitute(SUFFIX=self.suffix,PATH=path )
#         rg_logger.info("test conf:")
#         rg_logger.info(c)
#         with  open(self.xml_conf ,'w') as f :
#             f.write(c)
#
#     def impl(self):
#
#         if not os.path.exists(self.ini) :
#             raise  rigger_exception(" not found php.ini[%s]" %self.ini)
#         php = get_env_conf().php
#         cur_path=os.path.dirname(os.path.realpath(__file__))
#         phpunit_cmd  = """ %s -c %s %s/phpunit.php    """ %(php,self.ini,cur_path )
#         if len(self.conf)  == 0 :
#             self.build_conf()
#             cmd = "%s -c %s; rm %s" %(phpunit_cmd,self.xml_conf,self.xml_conf)
#         else:
#             cmd = "%s -c %s" %(phpunit_cmd,self.conf)
#         shexec.execmd(cmd)
#     def start(self):
#         if not hasattr(self,'called_start') :
#             self.called_start  = True
#             self.impl()
#     def reload(self):
#         self.start()
#
#     def shell(self):
#         if not hasattr(self,'called_shell') :
#             self.called_shell= True
#             self.impl()
#
#
#
#
# class dx_php(resource):
#     _ini    = "${PHP_INI}"
#     _script = None
#     def __init__(self,script=""):
#         self.script = script
#     def locate(self):
#
#         self.script = env_exp.value(self.script)
#         self.ini    = env_exp.value(self.ini)
#
#     def shell(self):
#         if not os.path.exists(self.ini) :
#             rg_logger.info( "dx_php first need php.ini not found %s" %self.ini)
#             self.ori_ini = self.ini
#             self.ini    =   env_exp.value("${PRJ_ROOT}/conf/used/console_php.ini")
#             if not os.path.exists(self.ini) :
#                 raise  rigger_exception(" dx_php not found php.ini[%s, %s]" %(self.ori_ini,self.ini))
#         php = get_env_conf().php
#         cmd = php + "  -c " + self.ini + " "  +  self.script
#         shexec.execmd(cmd)
#
# class host(resource):
#     def __init__(self,ip,domain):
#         self.ip = ip
#         self.domain=domain
#     def locate(self):
#         self.ip     = env_exp.value(self.ip)
#         self.domain = env_exp.value(self.domain)
#
#     def config(self):
#         path=os.path.dirname(os.path.realpath(__file__))
#         cmdtpl="$PYTHON $PATH/sysconf.py  -n $DOMAIN -f /etc/hosts  -t '#' -c '$IP $DOMAIN' "
#         c = Template(cmdtpl).substitute(PYTHON=get_env_conf().python,PATH=path,IP=self.ip,DOMAIN=self.domain)
#         shexec.execmd(c,True)
#
# class crontab(resource,svctag):
#     _key   = "${PRJ_NAME}_${APP_SYS}"
#     _cron  = None
#     def locate(self):
#         self.cron   = env_exp.value(self.cron)
#         self.key    = env_exp.value(self.key)
#         user        = env_exp.value("${USER}")
#         self.tmp_cron    = "/tmp/" + user + "_"  + self.key + ".cron"
#     def start(self):
#         self.append_conf()
#     def stop(self):
#         self.clean_conf()
#     def append_conf(self):
#         if not os.path.exists(self.cron):
#             raise rigger_exception("cron file not exists : %s" %self.cron)
#         cmdtpl= """
# crontab -l >  $ORI_CRON ;
# $PYTHON $CURPATH/sysconf.py  -n $KEY -f $ORI_CRON -t '#' -c $CRON -p file ;
# crontab $ORI_CRON
# """
#         path=os.path.dirname(os.path.realpath(__file__))
#         c = Template(cmdtpl).substitute(PYTHON=get_env_conf().python,CURPATH=path,KEY=self.key,
#                 ORI_CRON=self.tmp_cron,CRON=self.cron)
#         shexec.execmd(c,True)
#
#     def clean_conf(self):
#         cmdtpl= """
# crontab -l >  $ORI_CRON ;
# $PYTHON $CURPATH/sysconf.py  -n $KEY -f $ORI_CRON -t '#' -c ''  ;
# crontab $ORI_CRON
# """
#         path=os.path.dirname(os.path.realpath(__file__))
#         c = Template(cmdtpl).substitute(PYTHON=get_env_conf().python,CURPATH=path,KEY=self.key,
#                 ORI_CRON=self.tmp_cron,CRON=self.cron)
#         shexec.execmd(c,True)
#     pass
# class syslog(resource,svctag):
#     _append= None
#     _conf  = "/etc/syslog.conf"
#     _key   = "${PRJ_NAME}"
#     def __init__(self):
#         pass
#     def locate(self):
#         self.conf     = env_exp.value(self.conf)
#         self.append   = env_exp.value(self.append)
#         self.prj_name = env_exp.value(self.key)
#
#     def build_conf(self):
#         path=os.path.dirname(os.path.realpath(__file__))
#         cmdtpl="$PYTHON $PATH/sysconf.py  -n $NAME -f $CONF -t '#' -c '$APPEND' -p file "
#         c = Template(cmdtpl).substitute(PYTHON=get_env_conf().python,PATH=path,NAME=self.prj_name,
#                 APPEND=self.append,CONF=self.conf)
#         shexec.execmd(c,True)
#
#     def clean(self):
#         path=os.path.dirname(os.path.realpath(__file__))
#         cmdtpl="$PYTHON $PATH/sysconf.py  -n $NAME -f $CONF -t '#' -c '' "
#         c = Template(cmdtpl).substitute(PYTHON=get_env_conf().python,PATH=path,NAME=self.prj_name,
#                 CONF=self.conf)
#         shexec.execmd(c)
#         self.reload()
#     def start(self):
#         self.build_conf()
#         self.reload()
#     def stop(self):
#         self.clean()
#     def reload(self):
#         cmdtpl ="$SYSLOG_CTRL reload"
#         c = Template(cmdtpl).substitute(SYSLOG_CTRL=get_env_conf().syslog)
#         shexec.execmd(c,True)
#
#
# class links(resource):
#     links_map={}
#     def __init__(self,map):
#         self.ori_map = map
#
#     def locate(self):
#         links_map={}
#         for k ,v in self.ori_map.items():
#             k=  env_exp.value(k)
#             v=  env_exp.value(v)
#             self.links_map[k] = v
#     def config(self):
#         cmdtpl ="if test -L $DST ; then rm -rf  $DST ; fi ; dirname $DST | xargs mkdir -p ; ln -s  $SRC $DST"
#         for k ,v in self.links_map.items():
#             cmd = Template(cmdtpl).substitute(DST=k,SRC =v)
#             shexec.execmd(cmd)
#     def check(self):
#         for k ,v in self.links_map.items():
#             self.check_print(os.path.exists(k),k);
#
#     def clean(self):
#         cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi "
#         for k ,v in self.links_map.items():
#             cmd = Template(cmdtpl).substitute(DST=k,SRC =v)
#             shexec.execmd(cmd)
#
#
# class link(resource,filetag):
#     _force   = False
#     _dst     = ""
#     _src     = ""
#     def locate(self):
#         self.dst = env_exp.value(self.dst)
#         self.src = env_exp.value(self.src)
#
#     def config(self):
#         cmdtpl = ""
#         if self.force is True :
#             cmdtpl ="if test -L $DST ; then rm -rf  $DST ; fi ; dirname $DST | xargs mkdir -p ; ln -s  $SRC $DST"
#         else :
#             cmdtpl ="if ! test -L $DST ; then   dirname $DST | xargs mkdir -p ;  ln -s   $SRC $DST ; fi;  "
#         cmd = Template(cmdtpl).substitute(DST=self.dst,SRC =self.src)
#         shexec.execmd(cmd)
#
#     def clean(self):
#         self.check_print(os.path.exists(self.dst),self.dst);
#         cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi ; "
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         shexec.execmd(cmd)
#
#     def check(self):
#         self.check_print(os.path.exists(self.dst),self.dst)
#
#     def info(self):
#         return self.src
#
#
# class copy(resource,filetag):
#     _dst=None
#     _src=None
#     _force=True
#
#     def locate(self):
#         self.dst = env_exp.value(self.dst)
#         self.src = env_exp.value(self.src)
#
#     def config(self):
#         cmdtpl = ""
#         if self.force is True :
#             cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi ; dirname $DST | xargs mkdir -p ; cp -r  $SRC $DST"
#         else :
#             cmdtpl ="if ! test -e $DST ; then   dirname $DST | xargs mkdir -p ; cp -r  $SRC $DST ; fi;  "
#         cmd = Template(cmdtpl).substitute(DST=self.dst,SRC =self.src)
#         shexec.execmd(cmd)
#     def check(self):
#         self.check_print(os.path.exists(self.dst),self.dst)
#     def clean(self):
#         cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi ; "
#         cmd = Template(cmdtpl).substitute(DST=self.dst,SRC =self.src)
#         shexec.execmd(cmd)
#
# class path(resource,filetag):
#     _arr        = []
#     _dst        = None
#     _keep       = False
#     _chmod      = "a+w"
#     _auto_sudo  = False
#
#     def locate(self):
#         self.paths= []
#         if not self.dst is None:
#             self.paths.append( env_exp.value(self.dst))
#         for v in self.arr:
#             v=  env_exp.value(v)
#             self.paths.append( v )
#     def checkWrite(self,dst) :
#         while  True  :
#             if os.path.exists(dst) :
#                 return  os.access(dst, os.W_OK)
#             else :
#                 dst = os.path.dirname(dst)
#             if dst == "/"  or dst == "" or dst == "."  or dst == "./"  or dst ==  None :
#                 break
#         return False
#
#
#
#     def config(self):
#         for v in self.paths :
#             if os.path.exists(v)  and self.checkWrite(v) :
#                 continue
#             else :
#                 if not self.checkWrite(v) :
#                     if self.auto_sudo :
#                         self.sudo = True
#                     if not self.sudo :
#                         raise rigger_exception( "%s 没有写权限,也没有sudo 权限 " %(v) )
#             cmdtpl ="if test ! -e $DST; then   mkdir -p $DST ; fi ;   chmod $CHMOD  $DST; "
#             cmd = Template(cmdtpl).substitute(DST=v,CHMOD=self.chmod)
#             shexec.execmd(cmd)
#     def check(self):
#         for v in self.paths :
#             self.check_print(os.path.exists(v),v)
#     def clean(self):
#         if self.keep :
#             return
#         cmdtpl ="if  test -e $DST ; then rm -rf  $DST ; fi ;  "
#         for v in self.paths :
#             cmd = Template(cmdtpl).substitute(DST=v)
#             shexec.execmd(cmd)
#
#     def info(self):
#         if self.dst is None:
#             return ""
#         return self.dst
#
# class file_merge(resource,filetag):
#     """
#     生成文件列表
#     filter:  基于正则的过滤器
#     tpl:     内空模版
#     """
#     _dst        = None
#     _src        = None
#     _filter     = ".*\.conf"
#     _note       = "#"
#     _mod        = "a+w"
#     def locate(self):
#         self.dst        = env_exp.value(self.dst)
#         self.src        = env_exp.value(self.src)
#         self.note       = env_exp.value(self.note)
#         self.mod        = env_exp.value(self.mod)
#         self.filter     = env_exp.value(self.filter)
#     def config(self):
#         with open(self.dst, 'w+') as self.dstfile :
#             srclist = self.src.split(":")
#             for src in srclist:
#                 if not os.path.exists(src):
#                     raise inf.rigger_exception("not found this path: %s" %src)
#                 os.path.walk(src,self.proc_file,None)
#         if os.getuid() == os.stat(self.dst).st_uid :
#             # 其它人可以进行修改；
#             shexec.execmd("chmod %s %s " %(self.mod, self.dst))
#
#
#     def reload(self):
#         self.config()
#
#     def check(self):
#         self.check_print(os.path.exists(self.dst),self.dst)
#     def clean(self):
#         cmdtpl ="if  test -e $DST ; then rm -f $DST ;fi"
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         shexec.execmd(cmd)
#
#     def proc_file(self,arg,dirname,names):
#         names = sorted(names)
#         for n in names:
#             if re.match(self.filter, n):
#                 src_path = os.path.join(dirname , n )
#                 self.dstfile.write("\n%s file: %s\n" %(self.note,src_path))
#                 self.dstfile.write("%s ------------------------------\n" %(self.note))
#                 if not os.path.exists(src_path) :
#                     warn_msg = "file_merge %s not exists" %src_path
#                     print("warning:  %s" %warn_msg)
#                     rg_logger.warning(warn_msg)
#                     continue
#                 with open(src_path,'r') as srcfile :
#                     for line in srcfile:
#                         self.dstfile.write(line)
#
# class phpenv(resource):
#     _dst = "${PRJ_ROOT}/conf/used/${APP_SYS}_env.php"
#     def locate(self):
#         self.dst        = env_exp.value(self.dst)
#     def config(self):
#         content = """<?php
# class EnvConf {
# """
#         for k,v in os.environ.items() :
#             if re.match(r'\w+_HOME',k)  or re.match(r'PATH',k) or re.match(r'\w+_GIT',k) or re.match(r'.+\.git',v)  :
#                 continue
#             content +=  " const %-20s = '%s' ;\n"  %(k,v)
#         content += "\n}"
#         parent =   os.path.dirname(self.dst)
#         if not os.path.exists(parent) :
#             os.makedirs(parent)
#         with open(self.dst,'w') as dstfile :
#             dstfile.write(content)
#
# class merge(resource,filetag):
#     _files = []
#     _dst = None
#
#     def locate(self):
#         self.efiles= []
#         self.dst = env_exp.value(self.dst)
#         for v in self.files:
#             v=  env_exp.value(v)
#             self.efiles.append( v )
#     def config(self):
#         shexec.execmd(Template("cat /dev/null > $DST; " ).substitute(DST=self.dst))
#         cmdtpl ="cat $SRC >> $DST ;"
#         for v in self.efiles:
#             cmd = Template(cmdtpl).substitute(SRC=v,DST=self.dst)
#             shexec.execmd(cmd)
#     def check(self):
#         self.check_print(os.path.exists(self.dst),self.dst)
#     def clean(self):
#         cmdtpl ="if  test -e $DST ; then rm -f $DST ; fi  "
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         shexec.execmd(cmd)
#
#
# class autoload(resource,pylontag):
#     """build autoload data for pylon"""
#     _src     = None
#     _root    = ""
#     _dst     = "${RUN_PATH}"
#
#
#     def info(self):
#         return self.src
#     def locate(self):
#         self.src  = env_exp.value(self.src)
#         self.root = env_exp.value(self.root)
#         self.dst  = env_exp.value(self.dst)
#         self.out_clspath= os.path.join(self.root ,  self.dst ,  "_autoload_clspath.idx")
#         self.out_clsname= os.path.join(self.root ,  self.dst ,  "_autoload_clsname.idx")
#     def parse_cls(self,line):
#         res  = None
#         res1 =  re.search('(.*\.php):\s*(abstract)?\s*class\s+(\S+)',line)
#         res2 =  re.search('(.*\.php):\s*(interface)\s+(\S+)',line)
#         if res1 :
#             res=res1
#         if res2 :
#             res= res2
#         return res;
#
#     def config(self):
#         path=os.path.dirname(os.path.realpath(__file__))
#         #兼容: self.root 将没有意义
#         dst_path = os.path.join(self.root , self.dst)
#         cmd = Template("mkdir -p $DST").substitute( DST=dst_path)
#         shexec.execmd(cmd,False)
#         cls_tmp  = os.path.join(dst_path, "._find_cls.tmp")
#         shexec.execmd(Template('echo "" > $DST').substitute(DST=cls_tmp))
#         cmdtpl = 'find $SRC/ -name "*.php"   |  xargs  grep  -H -E "^ *(abstract)? *class "  >> $DST'
#         for  s in self.src.split(':') :
#             cmd = Template(cmdtpl).substitute( SRC = os.path.join( self.root ,  s) ,DST=cls_tmp)
#             shexec.execmd(cmd,False)
#         cmdtpl = 'find $SRC/ -name "*.php"   |  xargs  grep  -H -E "^ *interface "  >> $DST'
#         for  s in self.src.split(':') :
#             cmd = Template(cmdtpl).substitute( SRC =  os.path.join(self.root ,  s) ,DST=cls_tmp)
#             shexec.execmd(cmd,False)
#
#
#         auto_txt_file = os.path.join(self.root ,  self.dst ,  "_autoload_clspath.tmp")
#         with   open(auto_txt_file,'w') as autoload :
#             with  open(cls_tmp,'r') as find_cls :
#                 for line in find_cls.readlines():
#                     res  =  self.parse_cls(line)
#                     if not res :
#                         continue
#                     file_path=res.group(1)
#                     file_path= file_path.replace(self.root,'')
#                     cls =  res.group(3)
#                     autoload.write(Template("$CLS,$PATH\n").substitute(PATH=file_path,CLS=cls))
#             find_cls.close()
#         autoload.close()
#         shexec.execmd(Template("sort $SRC > $DST; rm $SRC ").substitute(SRC=auto_txt_file,DST=self.out_clspath))
#
#         auto_txt_file = os.path.join(self.root ,  self.dst ,  "_autoload_clsname.tmp")
#         with   open(auto_txt_file,'w') as autoload :
#             with  open(cls_tmp,'r') as find_cls :
#                 for line in find_cls.readlines():
#                     res  =  self.parse_cls(line)
#                     if not res :
#                         continue
#                     cls =  res.group(3)
#                     autoload.write(Template("cls_$LOWCLS,$CLS\n").substitute(CLS=cls,LOWCLS=cls.lower()))
#             find_cls.close()
#         autoload.close()
#         shexec.execmd(Template("sort $SRC > $DST; rm $SRC ").substitute(SRC=auto_txt_file,DST=self.out_clsname))
#
#     def check(self):
#         self.check_print(os.path.exists(self.out_clsname),self.out_clsname)
#         self.check_print(os.path.exists(self.out_clspath),self.out_clspath)
#
#     def clean_file(self,filename):
#         cmdtpl ="if test -e $DST ; then rm -f  $DST ; fi ; "
#         cmd = Template(cmdtpl).substitute(DST=filename)
#         shexec.execmd(cmd)
#     def clean(self):
#         self.clean_file(self.out_clspath)
#         self.clean_file(self.out_clsname)
#
# class rest(resource,pylontag):
#     _src = None
#     _dst = "${RUN_PATH}"
#     def locate(self):
#         self.src        = env_exp.value(self.src)
#         self.dst        = env_exp.value(self.dst)
#         self.out_idx    = os.path.join(self.dst , "_rest_conf.idx")
#     def config(self):
#
#         sed     = """sed -r "s/.+:class\s+(\S+)\s+.+\/\/\@REST_RULE:\s+(.+)/\\2 : \\1/g" """
#         cmdtpl  ="""grep --include "*.php"  -E "class .+ implements XService"  -R $SRC   |  """  + sed + " > $DST "
#         cmd     = Template(cmdtpl).substitute(SRC =  self.src ,DST=self.out_idx)
#         shexec.execmd(cmd,False)
#     def check(self):
#         self.check_print(os.path.exists(self.out_idx),self.out_idx)
#     def clean_file(self,filename):
#         cmdtpl ="if test -e $DST ; then rm -f  $DST ; fi ; "
#         cmd = Template(cmdtpl).substitute(DST=filename)
#         shexec.execmd(cmd)
#
#     def clean(self):
#         self.clean_file(self.out_idx)
#
# class action2(resource,pylontag):
#     """build action data for pylon"""
#     _src = None
#     _dst = "${RUN_PATH}"
#     _ini = "${PHP_INI}"
#     _autoload = "${RUN_PATH}"
#
#     def info(self):
#         return self.src
#     def locate(self):
#         self.src = env_exp.value(self.src)
#         self.dst        = env_exp.value(self.dst)
#         self.ini        = env_exp.value(self.ini)
#         self.out_idx    = os.path.join(self.dst , "_act_conf.idx")
#         self.autoload   = env_exp.value(self.autoload)
#
#     def config(self):
#         path=os.path.dirname(os.path.realpath(__file__))
#         cls_tmp = os.path.join(self.dst , "._act_cls.tmp")
#         out_tmp = os.path.join(self.dst , "._act_conf.tmp")
#         shexec.execmd('echo "" > %s' %cls_tmp)
#         cmdtpl1 = 'find $SRC -name "*.php"   |  xargs cat | grep "class Action_"  >> $DST'
#         for  s in self.src.split(':') :
#             cmd = Template(cmdtpl1).substitute(SRC =  s ,DST=cls_tmp)
#             shexec.execmd(cmd,False)
#         cmdtpl2 = "$PHP -c $INI  $CUR/build_action_conf.php  $AUTOLOAD  $IN  $OUT txt "
# #        pylon = get_env_conf().pylon
#         cmd = Template(cmdtpl2).substitute(PHP=get_env_conf().php ,CUR=path, INI= self.ini, IN=cls_tmp,
#                 OUT =  out_tmp,AUTOLOAD=self.autoload)
#         shexec.execmd(cmd,False)
#         clscmd = "sort %s > %s;   rm %s " %(out_tmp,self.out_idx,out_tmp)
#         shexec.execmd(clscmd)
#
#     def check(self):
#         self.check_print(os.path.exists(self.out_idx),self.out_idx)
#
#     def clean_file(self,filename):
#         cmdtpl ="if test -e $DST ; then rm -f  $DST ; fi ; "
#         cmd = Template(cmdtpl).substitute(DST=filename)
#         shexec.execmd(cmd)
#
#     def clean(self):
#         self.clean_file(self.out_idx)
#
# class action(resource,pylontag):
#     """build action data for pylon"""
#     _src = None
#     _dst = None
#     _ini = "${PHP_INI}"
#
#     def info(self):
#         return self.src
#     def locate(self):
#         self.src = env_exp.value(self.src)
#         if self.dst == None:
#             self.dst = self.src
#         self.dst = env_exp.value(self.dst)
#         self.ini = env_exp.value(self.ini)
#
#     def config(self):
#         path=os.path.dirname(os.path.realpath(__file__))
#         shexec.execmd(Template('echo "" > $DST/._act_cls.tmp').substitute(DST=self.dst))
#         cmdtpl1 = 'find $SRC -name "*.php"   |  xargs cat | grep "class Action_"  >> $DST/._act_cls.tmp'
#         for  s in self.src.split(':') :
#             cmd = Template(cmdtpl1).substitute(SRC =  s ,DST=self.dst )
#             shexec.execmd(cmd,False)
#         cmdtpl2 = "$PHP -c $INI  $CUR/build_action_conf_old.php  $DST/init.php  $DST/._act_cls.tmp $DST/_act_conf.tmp txt "
#         cmd = Template(cmdtpl2).substitute(PHP=get_env_conf().php ,INI= self.ini, CUR= path, DST =  self.dst)
#         shexec.execmd(cmd,False)
#         clscmd = "sort $DST/_act_conf.tmp > $DST/_act_conf.idx;  sort $DST/_act_conf.tmp > $DST/_act_conf.txt; rm $DST/_act_conf.tmp "
#         shexec.execmd(Template(clscmd).substitute(DST = self.dst))
#
#     def check(self):
#         action= self.dst+ "/_act_conf.idx"
#         self.check_print(os.path.exists(action),action)
#
#     def clean(self):
#         action= self.dst+ "/_act_conf.idx"
#         cmdtpl ="if test -e $DST ; then rm -f  $DST ; fi ; "
#         cmd = Template(cmdtpl).substitute(DST=action)
#         shexec.execmd(cmd)
#
# #class pylon_ui(resource):
# #    def __init__(self,web_inf,theme="brood"):
# #        self.web_inf = web_inf
# #        self.theme   = theme
# #    def locate(self):
# #        self.web_inf = env_exp.value(self.web_inf)
# #        self.theme   = env_exp.value(self.theme)
#
# #    def config(self):
# #        path=os.path.dirname(os.path.realpath(__file__))
# #        cmdtpl = "$PYLON/pylon_ui/setup.sh $SRC/scripts/  $SRC/styles  $SRC/images/  $THEME "
# #        cmd = Template(cmdtpl).substitute(PYLON = path + "/../" , SRC =  self.web_inf , THEME = self.theme )
# #        shexec.execmd(cmd)
#
#
#
# class module(controlor,rgtag):
#     """
# ------------eg:-----------------------
# common:
#     !R.module  &comm1
#         res:
#             - !R.path
#                 dst: "/tmp/test/pylon_rigger/${SYS_NAME}/1"
#                 chmod: "-R a+w"
#             - !R.path
#                 dst: "/tmp/test/pylon_rigger/${SYS_NAME}/2"
#                 chmod: "-R a+w"
#
# sys:
#     test:  !R.system
#         res:
#             - !R.vars
#                 defs:
#                     TEST_NAME: "${HOME}/devspace/pylon_rigger"
#                     SYS_NAME:  "test"
#             - !R.path
#                 dst: "/tmp/test/pylon_rigger"
#                 chmod: "-R a+w"
#             - *comm1
#     """
#     def resname(self):
#         if hasattr(self,'name'):
#             return  "%s(%s)" %(self.clsname(),self.name)
#         return self.clsname()
#
# class env(controlor,rgtag):
#     def resname(self):
#         if hasattr(self,'name'):
#             return  "%s(%s)" %(self.clsname(),self.name)
#         return self.clsname()
#
# class system( controlor,rgtag):
#     _allow_sys=None
#     def __init__(self, name, *args):
#         self.name = name
#         controlor.__init__(self,*args)
#     def allow(self):
#         allow_sys_arr = system.allow_sys.split(",")
#         for name  in  allow_sys_arr :
#             name=name.lstrip()
#             if name == "all"  or name == "ALL" or name == "@all" or name == "@ALL"  or name == self.name :
#                 return True
#         return False
#     def resname(self):
#         return  "%s(%s)" %(self.clsname(),self.name)
#     def locate(self):
#         # 注意，加入的倒序
#         self.lock_file = get_env_conf().run_path +   "/rgapp-${USER}-${PRJ_NAME}.lock"
#         p = path()
#         p.dst     = "${RUN_PATH}"
#         self.push(p)
#
#         # 先定义
#         v =vars()
#         v.RUN_PATH = "${PRJ_ROOT}/run/" + self.name
#         v.APP_NAME = self.name
#         self.push(v)
#
#     def start(self):
#         controlor.start(self)
#         shexec.execmd('sudo rm -rf ' +  env_exp.value(self.lock_file))
#     def stop(self):
#         shexec.execmd('sudo touch ' +  env_exp.value(self.lock_file))
#         controlor.stop(self)
#
# class environ_keeper :
#     def __enter__(self):
#         self.env = dict(os.environ)
#     def __exit__(self,*args,**kwargs):
#         os.environ.clear()
#         for k ,v in self.env.items():
#             os.environ[k] = v
#
# class system2(system):
#     def start(self):
#         with environ_keeper() :
#             system.start(self)
#     def stop(self):
#         with environ_keeper() :
#             system.stop(self)
#     def config(self):
#         with environ_keeper() :
#             system.config(self)
#
#     def reload(self):
#         with environ_keeper() :
#             system.reload(self)
#
#     def check(self):
#         with environ_keeper() :
#             system.check(self)
#
#     def clean(self):
#         with environ_keeper() :
#             system.clean(self)
#     def shell(self):
#         with environ_keeper() :
#             system.shell(self)
#
# class echo(resource):
#     _name = ""
#     _value= ""
#     def locate(self):
#         self.value= env_exp.value(self.value)
#     def config(self):
#         print(" rg-echo %s:%s" %(self.name,self.value))
#
# class vars(resource,rgtag):
#     def allow(self):
#         return True
#     def merge(self,other):
#         assert(isinstance(other,vars))
#         for k,v in other.__dict__.items():
#             if k[0:2] != "__":
#                 self.__dict__[k] = v
#     def define_vars(self):
#         items = {}
#         if  hasattr(self,'defs'):
#             items= self.defs
#         else:
#             items= self.__dict__
#         return items;
#
#     def assgin_value(self,key):
#         items = self.define_vars()
#         if items.has_key(key):
#             val = items[key]
#             if val == "${%s}" %key :
#                 msg =  "循环定义: %s = %s" %(key,val)
#                 rgio.simple_out(msg)
#                 return None
#             #递归付值
#             if god.debug >= 2 :
#                 rgio.simple_out( key + " = " + str(val))
#             val = env_exp.value(val,self.assgin_value)
#             os.environ[key] = val
#             rg_logger.info("set %s = %s " %(key,val))
#             return  val
#         return None
#
#     def locate(self):
#         items = self.define_vars()
#         for name , val in   items.items():
#             if re.match(r'__.+__',name):
#                 continue
#             name= name.upper()
#             self.assgin_value(name)
#
#
# def check_proc(svc, found_cmd,expect_cn="1"):
#     init=Template("V='-[ ]';SNAME=$NAME;PCNT=`$FOUND -c `; PCMD='$FOUND'; ").substitute(NAME=svc,FOUND=found_cmd)
#     rev=  init +  "if test $PCNT -ge " + expect_cn + "; then V='-[Y]'; fi ;"
#     cmd=  rev  +  """printf "%-100.90s%-20.20s%s\n" "$PCMD" "$SNAME($PCNT)" "$V" """
#     shexec.execmd(cmd)
#
# class php_res:
#
#     def export_env2php(self):
# #        os_env_str = "$_SERVER = array_merge($_SERVER, array(\n"
# #        for k,v in os.environ.items():
# #            if len(k) > 0  and k != "OS_ENV" and k != "SHELL" :
# #                os_env_str += ( "\t  %-20s => '%s',\n" %(k,v))
# #        os.environ['OS_ENV'] = os_env_str + "));"
#
#         """
#         导出RG的环境变量到 $PRJ_ROOT/tmp下。
#         当FPM启动时会把这个文件copy到Prefix下的env.conf
#         然后fpm_conf会include这个env.conf导入环境变量。
#         """
#         os.environ['OS_ENV'] = os_env_str = ''
#         tmpfile = env_exp.value("${PRJ_ROOT}/run/") + self.prefix + '.env'
#         for k,v in os.environ.items():
#             #预处理，清除掉Key的 " [ ] 空行和value的换行和 "
#             k = re.sub('[\'"\[\]\n]', '', k)
#             v = re.sub('[\"\n]', '', v)
#             if len(k) < 1 or len(v) < 1:
#                 continue
#             if k == "OS_ENV" or k == "SHELL" or k == '_':
#                 continue
#             os_env_str += ( 'env[%s] = "%s"\n' %(k,v))
#         if os.access(env_exp.value("${PRJ_ROOT}/run/"), os.W_OK) :
#             with open(tmpfile, 'w') as f: f.write (os_env_str)
#     def export_monitorconf(self, conf_path, files_to_check):
#         """ 为监控系统定义服务运行时生成的文件依赖并存入/var/run/{run_path}中 """
#         cmd = "cd %s;/home/q/tools/pylon_rigger/rigger restart -x %s" %( env_exp.value('${PRJ_ROOT}') , self.__class__.__name__)
#         prefix = os.path.dirname(conf_path)
#         if not os.path.isdir(prefix):
#            shexec.execmd("sudo mkdir -p '%s'" % prefix)
#         conf = 'FILES=\\"%s\\";' % files_to_check.replace(',', ' ') + 'CMD=\\"%s\\"' % cmd
#         shexec.execmd("sudo sh -c 'echo \"%s\" > \"%s\"'" %(conf, conf_path))
#     def export_fpmconf(self):
#         #如果非自定义fpm配置，那么生成
#         if not self.f_conf == self.fpm_conf:
#             fpm_conf = 'online' if self.fpm_conf == 'online' else 'dev'
#             cnt_min = str(int(self.fpm_cnt) - 10)
#             cnt_max = str(int(self.fpm_cnt) + 10)
#             #从conf_override中拼装配置并去掉环境修饰符,如：;online
#             conf_override = "\n".join(self.conf_override).replace(';' + fpm_conf, '')
#             tplpath = os.path.abspath(os.path.dirname(__file__) + '/../res_conf/fpm_svc.conf.' + fpm_conf)
#             #POOL_NAME=${prefix},FPM_CNT=${php_fpm_cnt},FPM_CNT_MIN=${php_fpm_cnt_min},FPM_CNT_MAX=${php_fpm_cnt_max}
#             tpl = open(tplpath, 'r').read()
#             tpl = Template(tpl).substitute(POOL_NAME=self.prefix,FPM_CNT=self.fpm_cnt,FPM_CNT_MIN=cnt_min,FPM_CNT_MAX=cnt_max,CONF_OVERRIDE=conf_override)
#             tmp_path = env_exp.value("${PRJ_ROOT}/run/" + self.f_conf.replace('/', '_'))
#             #生成到项目的tmp目录，然后sudo mv到指定位置
#             with open(tmp_path, 'w') as f: f.write (tpl)
#             shexec.execmd("sudo mv '%s' '%s'" % (tmp_path, self.f_conf))
#
# class fpm_svc(resource,php_res):
#     """
#     php-fpm 实现，使用unix socket作为监听地址(port)
#
#     php 5.3.10 中fpm可以使用的参数有
#     -y 指定fpm-conf的位置，这个是全局默认指定，随rigger发布，根据环境选择对应的cgi起始值的online/dev配置，可以在配置中覆盖
#     -p 此参数决定配置文件中相对路径的前置prefix，而非监听端口，简单来说 listen的sock文件地址为这个prefix加上conf中配置的值
#     -g pid文件位置，由于fpm无法用grep 特殊名称ini的方式来判断具体进程对应的项目，所以必须用pid对应项目路径来管理fpm进程
#
#     FPM配置规则  /var/run/$prefix/fpm.conf
#     监听地址规则 /var/run/$prefix/fpm.sock
#     PID位置规则  /var/run/$prefix/fpm.pid
#     环境变量导出 /var/run/$prefix/env.conf
#
#     启动fpm的例子
#     /usr/local/php-5.3/sbin/php-fpm -y path/to/php-fpm.conf  -p "/var/run/root-wan-fnt" -c /usr/local/php-5.3/lib/php.ini -g /var/run/root-wan-fnt/fpm.pid
#     """
#
#     #可配置项 fpm_conf：3个选项，dev|online|自定义路径
#     _fpm_conf   = "dev"
#     #可配置项 fpm_cnt : 10-1000 之内的整数，用来指定初始化fpm数量（dev环境时无效）
#     _fpm_cnt    = 20
#
#     #可配置项 sock_id：sock文件的id，概念很是纠结其实对应fpm参数的prefix，我们约定sock必需在 /var/run/目录下，
#     #而公共的fpm配置定死了sock的文件名为fpm.sock，所以我们最后的sock文件地址应该是 /var/run/${PREFIX}/fpm.sock
#     #但是直接抛出prefix概念，估计大家都看不懂，不如改个名叫做sock_id，当作sock在该APP_SYS的唯一id...
#     _sock_id    = ""
#     _php_ini    = "${PHP_INI}"
#
#     #可配置项 conf_override，可以给一个机会用来重定义fpm的某些细节配置，免去重新维护一套fpm配置的苦。
#     #注意只能重定义池实例级别的配置，global的不可以配置。例如：conf_override: - "user = ${USER}"
#     _conf_override = []
#
#     def locate(self):
#         self.prefix     = env_exp.value("rgapp-${USER}-${PRJ_KEY}-${APP_SYS}" + self.sock_id)
# #        rgio.simple_out("--------%s-------" %self.php_ini)
#         self.php_ini    = env_exp.value(self.php_ini)
# #        rgio.simple_out("--------%s-------" %self.php_ini)
#         self.fpm_conf   = env_exp.value(self.fpm_conf)
#         path=os.path.dirname(os.path.realpath(__file__))
#         if os.path.isfile(self.fpm_conf):
#             self.f_conf = self.fpm_conf
# #            self.prefix = '""' #当自定义fpm_conf时，prefix自动重置为空
#         elif self.fpm_conf == 'online' : #online环境用online conf, 使用rg tpl生成到prefix目录
#             self.f_conf = get_env_conf().run_path +  '/' + self.prefix + '/fpm_svc.conf.online'
#             if self.fpm_cnt < 10 or self.fpm_cnt > 1000 :
#                 self.fpm_cnt = 20
#         else : #其他一律使用dev的conf
#             self.f_conf = get_env_conf().run_path +  '/' + self.prefix + '/fpm_svc.conf.dev'
#         cmdtpl="sudo $PATH/fpm_ctrl.sh -b ${FPM_BIN} -c ${FPM_CONF} -f ${PHP_INI} -p ${PREFIX} -r ${PRJ_ROOT} -n ${FPM_CNT}"
#         self.base_cmd = Template(cmdtpl).substitute(PATH=path,FPM_BIN=get_env_conf().php_fpm,FPM_CONF=self.f_conf,PHP_INI=self.php_ini,PREFIX=self.prefix,PRJ_ROOT=env_exp.value('${PRJ_ROOT}'),FPM_CNT=self.fpm_cnt)
#     def config(self):
#         #init prefix dir
#         prefix_dir = get_env_conf().run_path   + '/' + self.prefix
#         if not os.path.isdir(prefix_dir):
#            shexec.execmd("sudo mkdir -p '%s'" % prefix_dir)
#         #export minitor
#         self.export_monitorconf(prefix_dir  + '/config.fpm', 'fpm.pid,fpm.sock')
#         #export env
#         self.export_env2php()
#         #then do config
#         #if fpm_conf is tpl, parse it first
#         self.export_fpmconf()
#         #else continue with custom fpm_conf
#         cmd = self.base_cmd+" -d config"
#         shexec.execmd(cmd)
#     def start(self):
#         cmd = self.base_cmd+" -d start"
#         shexec.execmd(cmd)
#     def stop(self):
#         cmd = self.base_cmd+" -d stop"
#         shexec.execmd(cmd)
#     def check(self):
#         cmdtpl = "cat " +  get_env_conf().run_path +  '/'   + self.prefix + "/fpm.pid 2>/dev/null | xargs ps | grep fpm"
#         cnt_cmd = Template(cmdtpl).substitute(FPM_CONF=self.f_conf)
#         check_proc("PHP-FPM", cnt_cmd, '1')
#     def reload(self):
#         cmd = self.base_cmd+" -d reload"
#         shexec.execmd(cmd)
#     def clean(self):
#         cmd = self.base_cmd+" -d clean"
#         shexec.execmd(cmd)
#     def restart(self):
#         cmd = self.base_cmd+" -d restart"
#         shexec.execmd(cmd)
#
# class using(controlor):
#     _ref   = None
#     _refs  = []
#     _args  = None
#     def locate(self):
#         if not self.obj_has('res'):
#             import copy
#             if self.obj_has('ref'):
#                 self.res = []
#                 self.res.append(copy.deepcopy(self.ref ))
#             elif self.obj_has('refs'):
#                 self.res = []
#                 for r  in self.refs :
#                     self.res.append(copy.deepcopy(r))
#             else:
#                 raise rigger_exception("using need ref args ")
#         if self.obj_has('args') and not self.obj_has is None:
#             cur_vars = self.args
#             if not isinstance(cur_vars,vars):
#                 raise rigger_exception("using.vars is not !R.vars ")
#             for s  in self.res :
#                 if  isinstance(s, vars) :
#                     s.merge(cur_vars)
#                 if  isinstance(s, controlor) :
#                     for sub_s in s.res:
#                         if  isinstance(sub_s, vars) :
#                             sub_s.merge(cur_vars)
#         controlor.locate(self)
#     pass
#
# class cgi_svc(resource,svctag):
#     _ip        = "127.0.0.1"
#     _port      = "9000"
#     _cgi_nu    = "2"
#     _proc_tag  = ""
#     _php_ini   = ""
#     _role      = "nobody"
#     def locate(self):
#         self.port    = env_exp.value(self.port)
#         self.cgi_nu =  env_exp.value(self.cgi_nu)
#         self.php_ini =  env_exp.value("${PHP_INI}")
#     def start(self):
#         cmdtpl="$SPAWN_FCGI -C $FCGI_NU -a $IP -p $PORT -u $ROLE -f \"$PHP_CGI  -c $PHP_INI \""
#         cmd = Template(cmdtpl).substitute( SPAWN_FCGI=get_env_conf().spawn_fcgi,
#                 FCGI_NU=self.cgi_nu, IP=self.ip,PORT= self.port,
#                 PHP_CGI=get_env_conf().php_cgi,ROLE=self.role ,
#                 PHP_INI=self.php_ini)
#         shexec.execmd(cmd)
#     def stop(self):
#         path=os.path.dirname(os.path.realpath(__file__))
#         cmdtpl="$PATH/kill_procs.sh $CMD $FILTER"
#         filter = self.php_ini
#         if not self.proc_tag == "" :
#             filter = self.proc_tag
#         cmd = Template(cmdtpl).substitute(PATH=path,CMD=get_env_conf().php_cgi, FILTER=filter )
#         shexec.execmd(cmd)
#         #dauble kill process!
#         shexec.execmd(cmd)
#     def check(self):
#         filter = self.php_ini
#         cmdtpl = "ps auxww | grep $CGI | grep  $FILTER "
#         cnt_cmd = Template(cmdtpl).substitute(CGI=get_env_conf().php_cgi,FILTER=filter)
#         check_proc("PHP-CGI", cnt_cmd,self.cgi_nu)
#
#     def reload(self):
#         self.stop()
#         self.start()
#
# def restart_op(obj):
#     obj.call_stop()
#     obj.call_start()
#
# first_beg = 1
# first_end = 2
#
# class runner:
#     prj={}
#     sys={}
#     env=None
#     def __init__(self):
#         self.runobjs = []
#
#     def reg_sys(self,sys):
#         self.sys = sys
#         for n,s in self.sys.items():
#             s.name = n
#     def reg_env(self,env):
#         self.env = env
#     def reg_prj(self,prj):
#         self.prj = prj
#
#     def set_default_res(self):
#         pass
#
#     def set_rg_vars(self):
#         if  not ( "hostname" in os.environ    or "HOSTNAME" in os.environ ) :
#             import socket
#             host = socket.gethostname()
#             os.environ['HOSTNAME'] = host
#         hostname    = os.environ['HOSTNAME']
#         nodes       = hostname.split('.')
#         if len(nodes) >= 3 :
#             os.environ['RG_IDC'] = nodes[-3]
#     def run_cmd(self,envname,sysname,allow_res,execmd,extra_res=None,sort=1):
#         system.allow_sys    =  sysname
#         resource.allow_res  =  allow_res
#         self.set_rg_vars()
#
#         rg_logger.debug("allow_res is %s" %allow_res)
#         if envname is not None:
#             envs = envname.split(',')
#             for e in envs :
#                 e = env_exp.value(e)
#                 if self.env.has_key(e):
#                     envobj = self.env[e]
#                     envobj.name = e
#                     if not os.environ.has_key('ENV'):
#                         os.environ['ENV'] = e
#                     self.runobjs.append(envobj)
#         self.set_default_res()
#         self.runobjs.append(self.prj)
#         extra_res_append = False
#         if sysname is not None:
#             if sysname == "all" or sysname == "ALL" or sysname == "_all" or sysname == "_ALL" :
#                 for n,s in self.sys.items():
#                     if not extra_res_append  and extra_res is not None:
#                         s.append(extra_res)
#                         extra_res_append = True
#                     self.runobjs.append(s)
#             else:
#                 namelist = sysname.split(',')
#                 if sort == first_end :
#                     namelist.reverse()
#                 for name in namelist :
#                     rg_logger.info("sys: %s" %name)
#                     if self.sys.has_key(name):
#                         s = self.sys[name]
#                         if not extra_res_append  and extra_res is not None:
#                             s.append(extra_res)
#                             extra_res_append = True
#                         self.runobjs.append(s)
#
#         else:
#             if extra_res is not None:
#                 self.runobjs.append(extra_res)
#         for r in self.runobjs :
#             execmd(r)
#         self.runobjs = []
#         return
#
#
# """
# """
#
# class prj(controlor,rgtag) :
#     def locate(self):
#         v =vars()
#         v.log_root =  get_env_conf().log_path    +   "/${PRJ_NAME}/"  + god.username()
#         v.run_root =  get_env_conf().run_path
#         self.append(v)
#         logpath = path()
#         logpath.auto_sudo   = True
#         logpath.keep        = True
#         logpath.dst         =  v.log_root
#         self.append(logpath)
#         runpaht           = path()
#         runpaht.auto_sudo = True
#         runpaht.keep      = True
#         runpaht.dst       = v.run_root
#         self.append(runpaht)
#
# def stop_service(name,pidfile,sudo=False):
#     path=os.path.dirname(os.path.realpath(__file__))
#     if sudo :
#         cmdtpl=" sudo %s/stop_proc.sh %s %s " %(path,pidfile,name)
#     else:
#         cmdtpl=" %s/stop_proc.sh %s %s " %(path,pidfile,name)
#     cmd = Template(cmdtpl).substitute(NAME=name,PID_FILE=pidfile)
#     shexec.execmd(cmd)
#
# class memcached(resource,svctag):
#     _ip        = "127.0.0.1"
#     _port      = "11211"
#     _mem       = "32"
#     def locate(self):
#         self.port    = env_exp.value(self.port)
#         self.ip      = env_exp.value(self.ip)
#         self.mem     = env_exp.value(self.mem)
#         prj_key      = env_exp.value("${PRJ_KEY}")
#         self.pid     = get_env_conf().run_path +   "/memcached_" + prj_key +"_" + self.port + ".pid"
#     def start(self):
#         cmdtpl="$MEMCACHED -d -m $MEM -u root -l $IP  -p$PORT -P $PID"
#         cmd = Template(cmdtpl).substitute( MEMCACHED=get_env_conf().memcached,
#                 IP=self.ip,PORT= self.port, PID=self.pid, MEM=self.mem)
#         shexec.execmd(cmd)
#     def stop(self):
#         if get_key("Are you share stop Memcached ? (y/N)" )  == "y" :
#             stop_service("Memcached",self.pid)
#     def reload(self):
#         print("reload memcached is ignore! ")
#     def check(self):
#         cmdtpl = "ps auxww | grep memcached | grep  $PORT  "
#         cmd = Template(cmdtpl).substitute(PORT=self.port)
#         check_proc("Memcached",cmd)
#
# class gearmand(resource,svctag):
#     _port      = "4730"
#     _extras    = ""
#     def locate(self):
#         self.port    = env_exp.value(self.port)
#         self.extras  = env_exp.value(self.extras)
#         prj_key      = env_exp.value("${PRJ_KEY}")
#         self.pid     = get_env_conf().run_path +   "/gearmand_" + prj_key +"_"  + self.port + ".pid"
#         self.log     = get_env_conf().log_path    +   env_exp.value("/${PRJ_NAME}/gearmand_" +  self.port + ".log")
#     def start(self):
#         cmdtpl="if ! test -s $PID ; then  $GEARMAND  -d -u root -p$PORT -P $PID -l $LOG $EXTRAS  ; fi"
#         cmd = Template(cmdtpl).substitute( GEARMAND=get_env_conf().gearmand,
#                 PORT= self.port, PID=self.pid,LOG=self.log,EXTRAS=self.extras)
#         shexec.execmd(cmd)
#     def stop(self):
#         if get_key("Are you share stop Gearmand ? (y/N)" )  == "y" :
#             stop_service("Gearmand ",self.pid)
#
#     def reload(self):
#         print("reload gearmand is ignore! ")
#         pass
#     def check(self):
#         cmdtpl = "ps auxww | grep gearmand | grep  $PORT  "
#         cmd = Template(cmdtpl).substitute(PORT=self.port)
#         check_proc("Gearmand",cmd)
#
# class shared_dict(resource,pylontag):
#     _name      = ""
#     _size      = 1
#     _dyn_load  = 1
#     _load_pgs  = 1
#     _file      = ""
#     _test  = "hello:hello"
#     def locate(self):
#         self.file   = env_exp.value(self.file)
#         self.test   = env_exp.value(self.test)
#     def start(self):
#         self.load_data()
#         pass
#     def stop(self):
#         path=os.path.dirname(os.path.realpath(__file__))
#         cmdtpl="sudo $PYTHON $RIGGER/sdict.py   -n $NAME -s $SIZE  -c $CMD $ARGS "
#         cmd = Template(cmdtpl).substitute( PYTHON=get_env_conf().python, RIGGER=path,NAME=self.name,SIZE=self.size, CMD="clean ",ARGS="" )
#         shexec.execmd(cmd)
#         pass
#     def reload(self):
#         self.load_data()
#         pass
#     def check(self):
#         key,val=self.test.split(":")
#         path=os.path.dirname(os.path.realpath(__file__))
#         cmdtpl="sudo $PYTHON $RIGGER/sdict.py   -n $NAME -s $SIZE  -c $CMD $ARGS "
#         cmd = Template(cmdtpl).substitute( PYTHON=get_env_conf().python, RIGGER=path,NAME=self.name,SIZE=self.size, CMD="find",ARGS="-k " + key  )
#         print( "expect value: "  +  val)
#         shexec.execmd(cmd)
#         pass
#     def load_data(self):
#         path=os.path.dirname(os.path.realpath(__file__))
#         cmdtpl="sudo $PYTHON $RIGGER/sdict.py   -n $NAME -s $SIZE  -c $CMD $ARGS "
#         cmd = Template(cmdtpl).substitute( PYTHON=get_env_conf().python, RIGGER=path,NAME=self.name,SIZE=self.size, CMD="load",ARGS="-f " + self.file )
#         shexec.execmd(cmd)
#
# class daemon_base(resource):
#     def config(self):
#         for i in range(1,self.worker + 1):
#             self.build_conf(self.ukeys[i],self.confs[i])
#
#     def start(self):
#         cmd_tpl = "$PYTHON  $ZDAEMON  -C $CONF  start "
#         for i in range(1,self.worker + 1):
#             conf = self.confs[i]
#             cmd     = Template(cmd_tpl).substitute(PYTHON=get_env_conf().python ,
#                     ZDAEMON = self.zdaemon,CONF= conf)
#             print ("start: " + self.program)
#             shexec.execmd(cmd)
#
#     def stop(self):
#         cmd_tpl = "$PYTHON  $ZDAEMON  -C $CONF  stop "
#         for i in range(1,self.worker + 1):
#             conf = self.confs[i]
#             cmd     = Template(cmd_tpl).substitute(PYTHON=get_env_conf().python ,
#                     ZDAEMON = self.zdaemon,CONF= conf)
#             shexec.execmd(cmd)
#     def check(self):
#         cmd_tpl = "ps auxww | grep zdaemon | grep  $CONF  | grep -v 'grep' "
#         for i in range(1,self.worker + 1):
#             conf = self.confs[i]
#             cmd     = Template(cmd_tpl).substitute(CONF= os.path.basename(conf))
#         check_proc("zdaemon",cmd)
# #       program 太长。。。
#         print ("program:" +  self.program)
#         main_cmd =  ""
#         for sub in self.program.split(' '):
#             if len(sub) > len(main_cmd):
#                 main_cmd = sub
#         cmd = Template("""ps auxww | grep -v "grep" | grep "$PROG" """).substitute(PROG= main_cmd )
#         check_proc("daemon_prog ",cmd)
#
#     def locate(self):
#         self.script     = env_exp.value(self.script)
#         self.logpath    = get_env_conf().log_path +  '/' + env_exp.value(self.logpath)
#         self.runpath    = env_exp.value(self.runpath)
#         self.zdaemon    = get_env_conf().zdaemon
#         self.worker     = int(env_exp.value(self.worker))
#         if not self.__dict__.has_key("main_ukey"):
#             import hashlib
#             self.main_ukey  = hashlib.md5(self.script +self.runpath ).hexdigest()
#         self.ukeys      = {}
#         self.confs      = {}
#
#         for i in range(1,self.worker + 1 ):
#             self.confs[i]       = self.runpath +  "/zdaemon-%d-%s.xml" %(i, self.main_ukey)
#             self.ukeys[i]       = "%s_%d" %(self.main_ukey,i)
#         self.program    = self.script
#     def build_conf(self,ukey,conf):
#         content = """
# <runner>
#     program         $SCRIPT
#     backoff-limit   10
#     daemon          $DAEMON
#     forever         $FOREVER
#     exit-codes      0,2
#     umask           022
#     directory       .
#     default-to-interactive True
#     hang-around     False
#     transcript      $LOG/zout.log.$UK
#     socket-name     $RUN_PATH/$UK.sock
# </runner>
#
# <eventlog>
#     level info
#     <logfile>
#     path $LOG/zrun.log.$UK
#     </logfile>
# </eventlog>
#
# <environment>
#  $ENVS
# </environment>
# """
#         envstr = ""
#         if  not ( "hostname" in os.environ    or "HOSTNAME" in os.environ ) :
#             import socket
#             host = socket.gethostname()
#             os.environ['hostname'] = host
#         for k,v in os.environ.items():
#             if k  == "PS1" :
#                 continue
#             v = v.strip()
#             #对于环境变量过滤非法字符
#             if not re.search(r"[\$\n<>]",v):
#                 envstr = envstr + "\t%s %s \n" %(k.upper() , v)
#         c = Template(content).substitute(SCRIPT=self.program, DAEMON=self.daemon,
#                 FOREVER=self.forever,LOG=self.logpath,UK=ukey,RUN_PATH=self.runpath,ENVS=envstr)
#         rg_logger.info("zdemon conf:")
#         rg_logger.info(c)
#         with  open(conf ,'w') as f :
#             f.write(c)
#
# class beanstalk (daemon_base):
#     _port     = "11300"
#     _ip       = "0.0.0.0"
#     _verbosity = False
#     _daemon   = "True"
#     _umask    = "022"
#     _forever  = "True"
#     _logpath  = "${PRJ_NAME}/"
#     _blog_root   = "/data/${PRJ_NAME}"
#     _runpath  = "${RUN_PATH}"
#     def locate(self):
#         self.worker     = 1
#         self.ip         = env_exp.value(self.ip)
#         self.blog_root  = env_exp.value(self.blog_root)
#         self.port       = env_exp.value(str(self.port))
#         self.beanstalkd = get_env_conf().beanstalkd
#         self.main_ukey  = "beanstalk-%s" %self.port
#         self.blog_path  = "%s/beanstalk-%s" %(self.blog_root, self.port)
#         self.script     = "%s -l %s -p%s -b %s " %(self.beanstalkd, self.ip,self.port,self.blog_path)
#         daemon_base.locate(self)
#     def config(self):
#
#         cmdtpl ="if test ! -e $DST; then   mkdir -p $DST ; fi ;   chmod a+rw $DST; "
#         cmd = Template(cmdtpl).substitute(DST=self.blog_path)
#         shexec.execmd(cmd)
#         daemon_base.config(self)
#
# class daemon (daemon_base):
#     _script   = ""
#     _daemon   = "True"
#     _umask    = "022"
#     _forever  = "True"
#     _logpath  = "${PRJ_NAME}/"
#     _runpath  = "${RUN_PATH}"
#     _worker   = 1
#
# class daemon_php(daemon_base):
#     _php_ini  = "${PHP_INI}"
#     _script   = ""
#     _daemon   = "True"
#     _umask    = "022"
#     _forever  = "True"
#     _logpath  = "${PRJ_NAME}/"
#     _runpath  = "${RUN_PATH}"
#     _worker   = 1
#
#     def locate(self):
#         daemon_base.locate(self)
#         self.php_ini    = env_exp.value(self.php_ini)
#         self.program    = "%s -c %s -f %s " %(get_env_conf().php,self.php_ini,self.script)
#
