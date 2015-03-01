#coding=utf8
from utls.rg_io import rgio
from rg_cmd_base import  rg_cmd , cmdtag_rg , cmdtag_prj ,cmdtag_pub
# import utls.rg_var
import res, rg_run ,rg_model ,rg_prj , interface



class help_cmd(rg_cmd,cmdtag_rg):
    def _execute(self,rargs):
        # ver  =  version(os.path.join(rargs.rg_root ,"version.txt" ))
        # rgio.simple_out("rigger ver: " + ver.info())
        cmdlen = len(rargs.prj.cmds)
        if cmdlen == 1 :
            # rargs.help()
            # list_cmd()
            return
        if cmdlen >= 2 :
            subcmd = rargs.prj.cmds[1]
            if subcmd == "res":
                if cmdlen == 3 :
                    resname = rargs.prj.cmds[2]
                    resobj = res.ins_res(resname)

                    # resobj.useage(output):
                    resobj.useage(rgio.simple_out)
        #TODO :

                # else:
                #     resouce.list_res()
            # elif subcmd == "remote":
            #     if len(sys.argv) == 4:
            #         n   = sys.argv[3]
            #         obj = ins_remote_cmd(n)
            #         obj._usage()
            #     else:
            #         list_remotecmd()
            # elif subcmd == "pub":
            #     if len(sys.argv) == 4:
            #         name = sys.argv[3]
            #         obj = ins_pub(name)
            #         obj._usage(rgio.simple_out)
            #     else:
            #         list_pub()
            #
            # elif subcmd == "tpl" :
            #     if len(sys.argv) == 4:
            #         name = sys.argv[3]
            #         obj = ins_tpl(name)
            #         obj._usage(rgio.simple_out)
            #     else:
            #         list_tpl()
            # else:
            #     _logger.debug("subcmd:%s" %subcmd)
            #     subcmd = ins_cmd(subcmd)
            #     subcmd._usage()



# class remote_cmd(rg_cmd, cmdtag_remote):
#     """
#     """
#     def _config(self,argv,rargs):
#         self.argv = argv
#         rg_cmd._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-p":
#                 rargs.prj = a
#             if o == "-u":
#                 rargs.user= a
#             if o == "-l":
#                 rargs.publish     = a
#             if o == "-t":
#                 rargs.tag= a
#             if o == "-h":
#                 rargs.host = a
#
#     def _execute(self,cmd,rargs):
#         if rargs.subcmd is None or len(rargs.subcmd) < 1 :
#             list_remotecmd()
#         else:
#
#             if rargs.prj is None:
#                 rargs.prj   = work_env().chose_project()
#             if rargs.prj is None:
#                 raise error.user_break("sorry, not project!")
#             cmds = rargs.subcmd[0].split(',')
#
#             project = work_env().fetch_project(rargs)
#
#             user = utls.env_exp.value("${USER}")
#             if project.pub_ver()  == 2 :
#                 import rg_pub.publish2
#                 self.pub    = rg_pub.publish2.publisher(rargs,project.publish_conf())
#                 publish_arr = self.pub.chose_publish(self.pub.load_conf())
#                 for publish in publish_arr:
#                     svrs    = publish.get_hosts(rargs.host)
#                     pkg     = publish.pkg
#                     deploy  = publish.deploy
#                     for cmd in  cmds :
#                         cmdobj = ins_remote_cmd(cmd)
#                         cmdobj.publish = publish
#                         cmdobj.svrs    = svrs
#                         cmdobj._config(self.argv,rargs)
#                         cmdobj.rg      = remote_rigger(deploy.root,pkg.lname(),user)
#                         rargs.subcmd = None
#                         cmdobj._execute(cmd,rargs)
#             elif project.pub_ver()  == 1 :
#                 import rg_pub.publish
#                 self.pub    = rg_pub.publish.publisher(rargs,project.publish_conf())
#                 publish_arr = self.pub.chose_publish(self.pub.load_conf())
#                 for publish in publish_arr:
#                     svrs  = publish.get_hosts(rargs.host)
#                     pkg   = self.pub.get_pkg(publish.pkg)
#                     lname = self.pub.lname(project,publish.pkg)
#                     for cmd in  cmds :
#                         cmdobj = ins_remote_cmd(cmd)
#                         cmdobj.publish = publish
#                         cmdobj.svrs    = svrs
#                         cmdobj._config(self.argv,rargs)
#                         cmdobj.rg      = remote_rigger(publish.inst.deploy.root,lname,publish.user)
#                         rargs.subcmd = None
#                         cmdobj._execute(cmd,rargs)
#
# class init_cmd(rg_cmd,cmdtag_rg):
#     """ åå§åç¯å¢ """
#     def _execute(self,cmd,rargs):
#         path=os.path.dirname(os.path.realpath(__file__))
#         path=os.path.dirname(path)
#         dst = os.getcwd() + "/_rg"
#         if os.path.exists(dst) :
#             print(" _rg å·²ç»å­å¨ï¼")
#             return
#         cmd = rg_shell.rg("tpl $SRC -o $DST")
#         cmd = Template(cmd).substitute(SRC=path + "/tpl" , DST=dst)
#         shexec.execmd(cmd)
#         cmd = """echo 'source /home/q/tools/rigger/rigger.rc' > $DST/_rigger.rc  """
#         cmd = Template(cmd).substitute(DST=os.getcwd())
#         shexec.execmd(cmd)
#
#
#
#
# class publish_base(rg_cmd,force_enable):
#     def _config(self,argv,rargs):
#         rg_cmd._config(self,argv,rargs)
#         rargs.repository = None
#         for o, a in argv.items():
#             if o == "-r":
#                 rargs.repository = a
#             if o == "-p":
#                 rargs.prj = a
#             if o == "-u":
#                 rargs.user= a
#             if o == "-l":
#                 rargs.publish     = a
#             if o == "-t":
#                 rargs.tag= a
#             if o == "-h":
#                 rargs.host = a
#             if o == "-f" and a == 0 :
#                 rargs.force = False
#
#     def _execute(self,cmd,rargs):
# #        self.pub         = publisher(rargs)
#         if rargs.prj is None:
#             rargs.prj   = work_env().chose_project()
#         if rargs.prj is None:
#             raise error.user_break("sorry, not project!")
# #        rargs.git   = env_exp.value("${G}")
#         self.project = work_env().fetch_project(rargs)
#         if self.project.pub_ver()  == 2 :
#             import rg_pub.publish2
#             self.pub = rg_pub.publish2.publisher(rargs,self.project.publish_conf())
#         elif self.project.pub_ver()  == 1 :
#             import rg_pub.publish
#             self.pub = rg_pub.publish.publisher(rargs,self.project.publish_conf())
#         if rargs.devtest  and rargs.tag   is not None :
#             rargs.tag   = "tmp_" + rargs.tag
#
# class remote_base:
#     svrs=[]
#     publish = None
#
# class cmd_bcmd(rg_cmd,publish_base,cmdtag_remote):
#     """
#     execute diy cmd for remote host
#     eg:
#         rg remote cmd -c "hello.sh"
#     """
#
#     def _config(self,argv,rargs):
#         self.argv = argv
#         rg_cmd._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-u":
#                 rargs.user= a
#             if o == "-h":
#                 rargs.host = a
#             if o == "-c":
#                 rargs.cmd= a
#     def _execute(self,cmd,rargs):
#         publish_base._execute(self,cmd,rargs)
#         user = utls.env_exp.value("${USER}")
#         if rargs.user is not None:
#             user = rargs.user
#         for s in self.svrs :
#             op = remote_op(s,user).ssh
#             self.host__execute(rargs,op,rargs.cmd)
#
#
# class info_bcmd(publish_base,remote_base,cmdtag_remote):
#     """
#     remote check publish plan svrs
#     """
#     def _execute(self,cmd,rargs):
#         publish_base._execute(self,cmd,rargs)
#         for s in self.svrs :
#             self.host__execute(rargs,self.rg.info,s)
#
# class reconf_bcmd(publish_base,remote_base,cmdtag_remote):
#     """
#     remote reconf system by  publish plan
#     """
#     def _config(self,argv,rargs):
#         for o, a in argv.items():
#             if o == "-e":
#                 rargs.env =  a
#             if o == "-s":
#                 self.sysname   = a
#
#     def _execute(self,cmd,rargs):
#         publish_base._execute(self,cmd,rargs)
#         for s in self.svrs:
#             self.host__execute(rargs,self.rg.reconf,s,rargs.env)
# #            self.rg.reconf(s,rargs.env)
#         pass
#
# class conf_bcmd(rg_cmd,publish_base,remote_base,cmdtag_remote):
#     """
#     remote conf  system by you input
#     rg  remote conf  -e online -s all
#     rg  remote conf,restart  -e online -s all
#     """
#     def _config(self,argv,rargs):
#         rg_cmd._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-e":
#                 rargs.env = a
#             if o == "-s":
#                 rargs.sysname   = a
#             if o == "-o":
#                 rargs.os_env    = a
#     def _execute(self,cmd,rargs):
#         publish_base._execute(self,cmd,rargs)
#         for s in self.svrs:
#             self.host__execute(rargs,self.rg.conf,s,rargs.env,rargs.sysname,rargs.os_env)
# #            self.rg.conf(s,rargs.env,rargs.sysname,rargs.os_env)
#         pass
#
# class restart_bcmd(publish_base,remote_base,cmdtag_remote):
#     """
#     reconf,restart prj for remote host
#     """
#     def _execute(self,cmd,rargs):
#         publish_base._execute(self,cmd,rargs)
#         for s in self.svrs:
#             self.rg.restart(s)
#
# class reload_bcmd(publish_base,remote_base,cmdtag_remote):
#     """
#     reload
#     """
#     def _execute(self,cmd,rargs):
#         publish_base._execute(self,cmd,rargs)
#         for s in self.svrs:
#             self.host__execute(rargs,self.rg.reload,s)
# #            self.rg.reload(s)
#         pass
#
#
# class reconf_cmd(run_base,cmdtag_run):
#     """
#     éæ°conf,æ¯æç¯å¢çè¿½å (+) ä¸å é¤(~)
#     rg reconf -e +debug ;
#     rg reconf -e ~debug ;
#     rg reconf -e +debug,~cache ;
#     """
#     def _config(self,argv,rargs):
#         run_base._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-e":
#                 rargs.env = modify_string(rargs.env,a)
#             if o == "-s":
#                 self.sysname   = a
#     def _execute(self,cmd,rargs):
#         run_base._execute(self,cmd,rargs)
#         execmd = lambda x,c :  call__config(x,c)
#         self.runner.run_cmd(rargs,execmd)
#         rargs.save()
#
#
#
#
#
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
#
# class tpl_cmd(dev_cmd,cmdtag_rg):
#     """
#     RG åç½®çæ¨¡æ¿å¼æ
#     rg tpl <tpl_path> [-o <out_path>]
#     """
#     def _config(self,argv,rargs):
#         dev_cmd._config(self,argv,rargs)
#         self.var_defs = ""
#         self.out_path = "./"
#         for o, a in argv.items():
#             if o == "-o":
#                 self.out_path = a
# #            if o == "-v":
# #                self.var_defs = a
#
#     def _execute(self,cmd,rargs):
#         import tpl.tplngin
#         self.root = rargs.subcmd[0]
#         if not os.path.exists(self.root) :
#             raise Exception("tpl cmd tplpath not exists : %s, %s" %(self.root,rargs.subcmd))
#         tpl.tplngin.tplworker()._execute(self.root,self.out_path)
#
#
#
#
# def ins_cmd(cmdkey):
#     rg_cmds = dir(cmds)
#     find_tag = cmdkey + "_cmd"
#     _logger.debug("input cmd: %s", find_tag)
#     if find_tag in rg_cmds:
#         exec "cmdobj = %s() " % find_tag
#         return cmdobj
#     return empty_cmd()
#
# def ins_remote_cmd(cmd):
#     rg_cmds = dir(cmds)
#     find_tag = cmd + "_bcmd"
#     _logger.debug("input cmd: %s", find_tag)
#     if find_tag in rg_cmds:
#         exec "cmdobj = %s() " % find_tag
#         return cmdobj
#     return empty_cmd()
#
#
# def ins_pub(name):
#     import pubconf
#     allpub = dir(pubconf)
#     if name in allpub:
#         exec "obj = pubconf.%s()" % name
#         return obj
#     return confbase()
#
# def ins_tpl(name):
#     import tplact
#     items  = dir(tplact)
#     if name in items:
#         exec "obj = tplact.%s()" % name
#         return obj
#     return confbase()
#
#
# def list_pub():
#     import rg_pub.pubconf
#     allres = rg_pub.pubconf.__dict__
#     rgio.prompt("all pub conf :" )
#     for k,v in allres.items() :
#         if isclass(v)  and issubclass(v,confbase):
#             output_confitems(k,v,"rg help pub")
#
# def list_tpl():
#     import tplact
#     allres = tplact.__dict__
#     rgio.prompt("all tpl conf :" )
#     for k,v in allres.items() :
#         if isclass(v)  and issubclass(v,confbase):
#             output_confitems(k,v,"rg help tpl")
#
#
# def list_tag_cmd(tag,taginfo):
#     allcmds = cmds.__dict__
#     rex = re.compile("(\w+)_cmd")
#     rgio.prompt("\n\t[%s] :" %taginfo)
#     for k,v in allcmds.items() :
#         if isclass(v) :
#             result = rex.match(v.__name__)
#             if result and issubclass(v,tag) :
#                 cmd =  result.groups()[0]
#                 exec "obj = %s_cmd()" % cmd
#                 output_confitems(cmd,obj,"rg help")
#
# def list_cmd():
#     list_tag_cmd(cmdtag_rg,"rigger  cmd")
#     list_tag_cmd(cmdtag_dev,"dev cmd")
#     list_tag_cmd(cmdtag_run,"run cmd")
#     list_tag_cmd(cmdtag_pub,"publish cmd")
#     list_tag_cmd(cmdtag_remote,"remote cmd")
#
# def list_remotecmd():
#     allcmds = cmds.__dict__
#     rex = re.compile("(\w+)_bcmd")
#     rgio.prompt("cmd list:")
#     for k,v in allcmds.items() :
#         if isclass(v) :
#             result = rex.match(v.__name__)
#             if result:
#                 rgio.prompt("\t\t%s" %result.groups()[0])
#
