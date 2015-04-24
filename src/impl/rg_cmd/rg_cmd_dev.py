#coding=utf8
from utls.rg_io import rgio , rg_logger
from rg_cmd_base import  rg_cmd , cmdtag_rg , cmdtag_prj ,cmdtag_pub
import interface
import utls.rg_var , utls.dbc , utls.check
import res
import res.node
import conf

class dev_cmd_base :
    def _config(self,argv,rargs):
        pass

    def loadconf(self,rargs) :
        # import  pdb
        # pdb.set_trace()
        import utls.rg_yaml,copy
        utls.dbc.must_exists(rargs.dev.conf)
        rg_logger.info("load prj conf: %s" %(rargs.dev.conf))
        loader   = utls.rg_yaml.conf_loader(rargs.dev.conf)
        data     = loader.load_data("!C","conf")
        dev_data = data['_dev']
        for confobj in dev_data :
            confobj._load()
        # context = interface.run_context()


class ci_cmd(dev_cmd_base) :
    def _execute(self,rargs):
        self.loadconf(rargs)
        conf.version.ins().update_ver()
        conf.version.ins().save()
        ver =  conf.version.ins().info()
        conf.git.ins().commit(ver,rargs.dev.message)
        conf.git.ins().push()

class rc_cmd(dev_cmd_base) :
    def _execute(self,rargs):
        self.loadconf(rargs)
        conf.version.ins().update_ver()
        conf.version.ins().save()
        ver =  conf.version.ins().info()
        conf.git.ins().commit(ver,rargs.dev.message)
        conf.git.ins().push()
        conf.git.ins().set_tag(ver)

    # ver = self.prj.get_version()
    #  if not confirm("ä½ ç¡®è®¤è¦<81>å<80><99>é<80><89>å<8f><91>å¸<83>æ­¤ç<89><88>æ<9c>¬ä¹<88> [%s]?" %ver)   :
    #      return
    #
    #  if hasattr(self.prj.hook,'rc_before') :
    #      self.prj.do_hook(self.prj.hook.rc_before,"rc before")
    #  if confirm("ä½ é<9c><80>è¦<81>æ<9b>´æ<96>°ç<89><88>æ<9c>¬å<8f>·,å¹¶æ<8f><90>äº¤ä»£ç <81>ä¹<88>?" )   :
    #      self.prj.up_version()
    #      ver = self.prj.get_version()
    #      work_env.scm().commit(ver,rargs.message)
    #  work_env.scm().push()
    #  tag = ver
    #  if rargs.devtest :
    #      tag = "tmp_" + ver
    #  _logger.info("rg rc tag: %s" %tag)
    #  work_env.scm().set_tag(tag)   ass

