
# class init_bcmd(publish_base,remote_base,cmdtag_remote):
#     def _execute(self,cmd,rargs):
#         publish_base._execute(self,cmd,rargs)
#         self.pub.init(self.publish,self.svrs)
#         pass
#
# class pub_cmd(publish_base,cmdtag_pub):
#     """
#     åå¸é¡¹ç® åæ° -t -l -h:
#     * -t <tag> , æ¯æé¨ä»½å¹é  -t 1.0.0.360  -t 1.0
#     * -l <plan>
#     * -h <host>  host:  ip,æºå¨å å å¼ç¨ ä¾ï¼ -h 127.0.0.1 -h w1.game.com -h @group/work
#     """
#     def _execute(self,cmd,rargs):
#         publish_base._execute(self,cmd,rargs)
#         self.pub.pub(self.project)
#
#
#
# class patch_cmd(publish_base,cmdtag_pub):
#     """
#     patch system
#     """
#     def _execute(self,cmd,rargs):
#         publish_base._execute(self,cmd,rargs)
#         self.pub.patch(self.project)
#
#
#
# class project_base(rg_cmd):
#     def _execute(self,cmd,rargs):
#         if rargs.prj is None:
#             rargs.prj  = os.path.basename(os.getcwd())
#         _logger.info("conf.yaml is %s" ,rargs.conf)
#         self.prj = rg_project(rargs.prj, rargs.conf)
#
#
# class showconf_cmd(project_base,cmdtag_run):
#     """
#     æ¥çå½åéç½®
#     """
#     def _execute(self,cmd,rargs):
#         project_base._execute(self,cmd,rargs)
#         rgio.simple_out(str(rargs))
#
# class dev_cmd(project_base):
#     def _config(self,argv,rargs):
#         rg_cmd._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-m":
#                 rargs.message = a
#             if o == "-w":
#                 rargs.devtest = True
#     def _execute(self,cmd,rargs):
#         project_base._execute(self,cmd,rargs)
#         pass
#
# class tag_cmd(dev_cmd,cmdtag_dev):
#     " rg tag "
#     def _execute(self,cmd,rargs):
#         dev_cmd._execute(self,cmd,rargs)
#         ver = self.prj.get_version()
#         work_env.scm().set_tag(ver)
#
# class info_cmd(project_base,cmdtag_run):
#     "æ¥çå½åé¡¹ç®çç¶åµ"
#     def _execute(self,cmd,rargs):
#         project_base._execute(self,cmd,rargs)
#         rgio.prompt("version: " + self.prj.version())
#         if rargs.is_config :
#             rgio.prompt("conf: %s" % str(rargs))
#         showconf_cmd()._execute("showconf",rargs)
#         check_cmd()._execute("check",rargs)
#
#     pass
#
# class ver_cmd(dev_cmd,cmdtag_dev):
#     def _execute(self,cmd,rargs):
#         dev_cmd._execute(self,cmd,rargs)
#         self.prj.up_version()
#
# class ci_cmd(dev_cmd,cmdtag_dev):
#     """
#     è¿ç¨æäº¤ä»£ç 
#     rg ci -m ""
#     """
#     def _execute(self,cmd,rargs):
#         dev_cmd._execute(self,cmd,rargs)
#         if hasattr(self.prj.hook,'ci_before') :
#             self.prj.do_hook(self.prj.hook.ci_before,"ci before")
#         self.prj.up_version()
#         ver = self.prj.get_version()
#         work_env.scm().commit(ver,rargs.message)
#         work_env.scm().push()
#         pass
#     pass
#
# class rc_cmd(dev_cmd,cmdtag_dev):
#     """
#     æäº¤åé. ä»£ç å¨åæ´çæ¬åï¼æä¸TAG å¹¶æäº¤è¿ç¨
#     rg rc
#     rg rc -m "XP relase"
#     """
#     def _execute(self,cmd,rargs):
#
#         dev_cmd._execute(self,cmd,rargs)
#         # import pdb
#         # pdb.set_trace() ;
#         ver = self.prj.get_version()
#         if not confirm("ä½ ç¡®è®¤è¦åéåå¸æ­¤çæ¬ä¹ [%s]?" %ver)   :
#             return
#
#         if hasattr(self.prj.hook,'rc_before') :
#             self.prj.do_hook(self.prj.hook.rc_before,"rc before")
#         if confirm("ä½ éè¦æ´æ°çæ¬å·,å¹¶æäº¤ä»£ç ä¹?" )   :
#             self.prj.up_version()
#             ver = self.prj.get_version()
#             work_env.scm().commit(ver,rargs.message)
#         work_env.scm().push()
#         tag = ver
#         if rargs.devtest :
#             tag = "tmp_" + ver
#         _logger.info("rg rc tag: %s" %tag)
#         work_env.scm().set_tag(tag)
#         pass
#
#
# class runctrl_cmd(project_base):
#     def _execute(self,cmd,rargs):
#         project_base._execute(self,cmd,rargs)
#         self.prj.using_os(rargs.os_env)
#         runner = self.prj.prj_runner()
#         runner.run(rargs.env,cmd,rargs.sysname,rargs.allow_res,rargs.script)
#         if cmd == "config" or cmd == "conf" :
#             rargs.is_config  = True
#             rargs.save()
#
# class run_base(project_base):
#     def __init__(self):
#         self.need_compatible = True
#     def _execute(self,cmd,rargs):
# #        print(self.need_compatible)
# #        print(self.compatible)
#         if self.need_compatible and  rargs.compatible is False :
#             raise error.rigger_exception("sorry, not compatible , please conf again")
#         project_base._execute(self,cmd,rargs)
#         self.prj.using_os(rargs.os_env)
#         self.runner = self.prj.prj_runner()
#         self.runner.context.prj_root = self.prj.root
#
# class resconf_able:
#     def _config(self,argv,rargs):
#         for o, a in argv.items():
#             if o == "-e":
#                 rargs.env = a
#             if o == "-s":
#                 rargs.sysname   = a
#             if o == "-o":
#                 rargs.os_env    = a
#
#
# class depend_cmd(run_base,cmdtag_run):
#     """
#     æ£æ¥ä¾èµ rg depend -e <env> -s <sys> -o <os>"
#     """
#     def _config(self,argv,rargs):
#         run_base._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-e":
#                 rargs.env = a
#             if o == "-s":
#                 rargs.sysname   = a
#             if o == "-o":
#                 rargs.os_env    = a
#             if o == "-x":
#                 rargs.allow_res= a
#                 _logger.info("allow resource is %s" %rargs.allow_res)
#
#     def _execute(self,cmd,rargs):
#         self.need_compatible = False
#         run_base._execute(self,cmd,rargs)
#         execmd = lambda x,c :  call_depend(x,c)
#         self.runner.run_cmd(rargs,execmd)
