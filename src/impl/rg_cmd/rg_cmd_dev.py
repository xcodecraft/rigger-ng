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
        print(argv)
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


