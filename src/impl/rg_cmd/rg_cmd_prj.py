#coding=utf8
from utls.rg_io import rgio
from rg_cmd_base import  rg_cmd , cmdtag_rg , cmdtag_prj ,cmdtag_pub
import utls.rg_var , interface
from impl.rg_prj import *

class prj_cmd_base :
    def _config(self,argv,rargs):
        self.env = []
        if argv.has_key('-e') :
            self.env = argv['-e'].split(',')
        else:
            self.env = rargs.prj.env.split(',')

        self.sys = []
        if argv.has_key('-s') :
            self.sys = argv['-s'].split(',')
        else:
            self.sys = rargs.prj.sys.split(',')

    def runcmd(self,rargs,fun) :
        import impl.rg_yaml,copy
        loader = impl.rg_yaml.conf_loader(rargs.prj.conf)
        data   = loader.load_data("!R","res")

        env_data    = data['__env']
        prj_data    = data['__prj']
        sys_data    = data['__sys']

        main  = impl.rg_prj.prj_main()
        if len(self.env) == 0 :
            return
        for env in self.env :
            for env_obj  in env_data :
                if env_obj.name == env :
                    main.append(env_obj)
        main.append(prj_data)
        context = interface.run_context()
        interface.control_call(main,fun,context)

        for sys in self.sys :
            for sysobj in   sys_data :
                if  sysobj.name ==  sys :
                    interface.control_call(sysobj,fun,context)

class info_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg info
    """
    def _execute(self,rargs):
        rgio.struct_out("rg %s" %(rargs) )
        self.runcmd(rargs,lambda x , y : x._info(y))

class conf_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg conf -e <env> -s <sys> [-o <os>] "
    rg conf -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x , y : x._config(y))

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


# class php_cmd(run_base,resconf_able,cmdtag_run):
#     """execut php eg: rg php -f 'xxx.php arg1 arg2'  """
#     def _config(self,argv,rargs):
#         run_base._config(self,argv,rargs)
#         resconf_able._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-f":
#                 rargs.script = a
#     def _execute(self,cmd,rargs):
#         run_base._execute(self,cmd,rargs)
#         if  rargs.script is None or len(rargs.script)  == 0 :
#             raise error.rigger_exception(" need -f  argu")
#         dxphp   = resouce.dx_php(rargs.script.lstrip())
#         execmd  = lambda x,c :  call_shell(x,c)
#         self.runner.run_cmd(rargs,execmd,dxphp)
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
# class shell_cmd(run_base,resconf_able, cmdtag_run):
#     """execut shell eg: rg shell -f 'xxx.sh arg1 arg2' """
#     def _config(self,argv,rargs):
#         run_base._config(self,argv,rargs)
#         resconf_able._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-f":
#                 rargs.script = a
#     def _execute(self,cmd,rargs):
#         run_base._execute(self,cmd,rargs)
#         if rargs.script is None or len(rargs.script)  == 0 :
#             raise error.rigger_exception(" need -f  argu")
#         dxshell = resouce.dx_shell(vars(),rargs.script.lstrip())
#         execmd = lambda x,c :  call_shell(x,c)
#         self.runner.run_cmd(rargs,execmd,dxshell)
#     def _usage(self):
#         rgio.prompt('usage: shell -f <script>')
#         rgio.prompt('eg: rg shell -f "test/test_run.sh -a -b -c "')
