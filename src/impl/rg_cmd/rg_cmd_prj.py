#coding=utf8
from utls.rg_io import rgio , rg_logger
from rg_cmd_base import  rg_cmd , cmdtag_rg , cmdtag_prj ,cmdtag_pub
import interface
import utls.rg_var , utls.dbc , utls.check
import res
import res.node
import os

class prj_cmd_base(rg_cmd) :
    def _config(self,argv,rargs):
        self.env = []
        if argv.has_key('-e') :
            self.env = argv['-e'].split(',')
        if rargs.prj.env :
            self.env = rargs.prj.env.split(',')

        self.sys = []
        if argv.has_key('-s') :
            self.sys = argv['-s'].split(',')
        if rargs.prj.sys:
            self.sys = rargs.prj.sys.split(',')


    @staticmethod
    def check_data(data):
        utls.check.not_none(data ,"project no yaml data")
        utls.check.must_true(data.has_key('_env'),"project no _env data")
        utls.check.must_true(data.has_key('_sys'),"project no _sys data")
        return True

    def runcmd(self,rargs,fun,extra=None) :
        import utls.rg_yaml,copy
        utls.dbc.must_exists(rargs.prj.conf)
        rg_logger.info("load prj conf: %s" %(rargs.prj.conf))
        loader = utls.rg_yaml.conf_loader(rargs.prj.conf)
        data   = loader.load_data("!R","res")
        prj_cmd_base.check_data(data)

        env_data    = data['_env']
        sys_data    = data['_sys']

        if data.has_key('_mod') :
            for m  in  data['_mod'] :
                res.node.regist_mod(m)


        main  = res.prj_main()
        if len(self.env) == 0 :
            return
        #import pdb
        #pdb.set_trace()
        for env in self.env :
            for env_obj  in env_data :
                res.node.env_regist(env_obj)
                if env_obj._name == env :
                    main.append(env_obj)
        context = interface.run_context()
        # interface.control_call(main,fun,context)

        extra_used = False
        if len(self.sys) > 0 :
            for sys in self.sys :
                for sysobj in   sys_data :
                    res.node.sys_regist(sysobj)
                    if  sysobj._name ==  sys :
                        # 传入的外部res
                        if not extra_used and  extra is not None :
                            sysobj.append(extra)
                            extra_used = True
                        main.append(sysobj)

        interface.control_call(main,fun,context,"unknow")

class info_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg info
    """
    def _execute(self,rargs):
        rgio.struct_out("rg %s" %(rargs) )
        rgio.struct_out("")
        self.runcmd(rargs,lambda x , y : x._info(y))

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

class data_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg data -e <env> -s <sys> [-o <os>] "
    rg data -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._data(y))

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
#
# class phpunit_cmd(run_base,resconf_able, cmdtag_run):
#     """execut php eg: rg phpunit -f '<your.xml> | <test path>'  """
#     def _config(self,argv,rargs):
#         run_base._config(self,argv,rargs)
#         resconf_able._config(self,argv,rargs)
#         rargs.script = ""
#         for o, a in argv.items():
#             if o == "-f":
#                 rargs.script = a
#     def _execute(self,cmd,rargs):
#         run_base._execute(self,cmd,rargs)
#         punit = resouce.phpunit(rargs.script.lstrip())
#         execmd = lambda x,c :  call_shell(x,c)
#         self.runner.run_cmd(rargs,execmd,punit)
#
