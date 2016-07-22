#coding=utf8
from utls.rg_io import rgio , rg_logger
from rg_cmd_base import  rg_cmd , cmdtag_rg , cmdtag_prj ,cmdtag_pub
import interface
import utls.rg_var , utls.dbc , utls.check
import res
import res.node
import os
import conf.run_conf 

class prj_cmd_base(rg_cmd) :
    def _config(self,argv,rargs):
        self.passwd = None 
        self.env = []
        if argv.has_key('-e') :
            self.env = argv['-e'].split(',')
        if rargs.prj.env :
            self.env = rargs.prj.env.split(',')

        self.sys = []
        if argv.has_key('-s') :
            self.sys = argv['-s'].split(',')

        if argv.has_key('-p') :
            self.passwd= argv['-p']
        if rargs.prj.sys:
            self.sys = rargs.prj.sys.split(',')




    def runcmd(self,rargs,fun,extra=None) :
        utls.check.must_exists(rargs.prj.conf)
        conf.run_conf.load(rargs.prj.conf)


        main  = res.prj_main()
        if len(self.env) == 0 :
            return
        #import pdb
        #pdb.set_trace()
        


        for  need_env in self.env :
            obj = res.node.env_find(need_env)
            if obj is None :
                obj = interface.res_proxy(res.node.env_find,need_env,"env")
            main.append(obj)

        if len(self.sys) > 1 and extra is not None :
                raise interface.rigger_exception("forbit! execute in muti sys(%s)" %(self.sys))

        for need_sys in self.sys :
            obj = res.node.sys_find(need_sys)
            if obj is None :
                obj = interface.res_proxy(res.node.sys_find,need_sys,"sys")
            main.append(obj)
            if extra is not None :
                obj.append(extra)

        context        = interface.run_context()
        context.passwd = self.passwd
        project        = res.project()
        project.setup4start(context)
        interface.control_call(main,fun,context,"unknow")

class info_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg info [-l level] [-a 1 ]
    """
    def _config(self,argv,rargs):
        prj_cmd_base._config(self,argv,rargs)
        self.level = 2 
        if argv.has_key('-l') :
            self.level = (int)(argv['-l'] )
        if argv.has_key('-a') :
            self.env = "@all"
            self.sys = "@all"

    def _execute(self,rargs):
        rgio.struct_out("rg %s" %(rargs) )
        rgio.struct_out("")
        self.runcmd(rargs,lambda x , y : x._info(y,self.level))

class conf_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg conf -e <env> -s <sys> [-o <os>] "
    rg conf -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x , y : x._config(y))
        # rars_file = os.getcwd() + "/_rg/.rigger-ng-v1.data"
        rargs.save()

class reconf_cmd(conf_cmd):
    """
    rg reconf
    """
    pass

class start_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg start -e <env> -s <sys> [-o <os>] "
    rg start -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._start(y))

class stop_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg stop -e <env> -s <sys> [-o <os>] "
    rg stop -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._stop(y))

class clean_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg clean -e <env> -s <sys> [-o <os>] "
    rg clean -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._clean(y))


class check_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg check -e <env> -s <sys> [-o <os>] "
    rg check -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._check(y))

class restart_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg restart -e <env> -s <sys> [-o <os>] "
    rg restart -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._stop(y))
        self.runcmd(rargs,lambda x,y : x._start(y))

class reload_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg reload -e <env> -s <sys> [-o <os>] "
    rg reload -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._reload(y))

def allow_res(c) :
    return True

class php_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg php -f 'xxx.php' -a "args"  -i <php.ini> -b <php.bin>
    rg php -f 'xxx.php' -a "args   -e <env> -s <system> 
    """
    def _config(self,argv,rargs):
        self.ini     = None
        self.bin     = None
        self.args    = ""
        rargs.script = ""
        prj_cmd_base._config(self,argv,rargs)
        for o, a in argv.items():
            if o == "-f":
                rargs.script = a
            if o == "-i":
                self.ini = a
            if o == "-b":
                self.bin = a
            if o == "-a" : 
                self.args = a 

        if  not os.path.exists(rargs.script)  :
            raise interface.cmd_use_error("php","rg php  script['%s'] not exists   " %(rargs.script))
    def _execute(self,rargs):
        phpres        = res.php()
        phpres.script = rargs.script
        phpres.args   = self.args 
        if self.bin is not None :
            phpres.bin    = self.bin
        if self.ini is not None :
            phpres.ini    = self.ini
        execmd        = lambda x,c :  x._start(c)
        phpres._allow = allow_res
        interface.resource.allow_res = 'no'
        self.runcmd(rargs,execmd,phpres)

class phpunit_cmd(php_cmd):
    """rg phpunit -t <tc>   -s <system>  
       eg:
       rg phpunit -t test/cases2.0/price_test.php  -s test
    """
    def _config(self,argv,rargs):
        tc_file   = ""
        bootstrap = "./test/bootstrap.php"
        for o, a in argv.items():
            if o == "-t":
                tc_file = a
        argv['-f'] = "/usr/local/php/bin/phpunit"
        argv['-a'] = " --bootstrap  %s %s" %(bootstrap , tc_file)
        php_cmd._config(self,argv,rargs)
                


class shell_cmd(prj_cmd_base,cmdtag_prj):
    """
        rg shell -f xxx.sh  '
        rg shell -f xxx.sh  -u 'arg1 arg2'
    """
    def _config(self,argv,rargs):
        prj_cmd_base._config(self,argv,rargs)
        self.args = None
        for o, a in argv.items():
            if o == "-f":
                rargs.script = a
            if o == "-u":
                self.args = a
        if  not os.path.exists(rargs.script)  :
            raise interface.cmd_use_error("shell","rg php  script['%s'] not exists   " %(rargs.script))
    def _execute(self,rargs):
        shres        = res.shell()
        shres.script = rargs.script
        if self.args is not None :
            shres.args = self.args
        execmd       = lambda x,c :  x._start(c)
        shres._allow = allow_res
        interface.resource.allow_res = 'no'
        self.runcmd(rargs,execmd,shres)

