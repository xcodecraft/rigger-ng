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

    def useage(self,output):
        if hasattr(self,"__doc__") and self.__doc__ is not None:
            output(str(self.__doc__))
        else:
            output("%s has no more info" % self.__class__)

    def loadconf(self,rargs) :
        import utls.rg_yaml,copy
        utls.dbc.must_file(rargs.dev.conf)
        rg_logger.info("load prj conf: %s" %(rargs.dev.conf))
        loader   = utls.rg_yaml.conf_loader(rargs.dev.conf)
        data     = loader.load_data("!C","conf")
        dev_data = data['_dev']
        for confobj in dev_data :
            confobj._load()


class ci_cmd(dev_cmd_base) :
    """
    提交代码
    rg ci -m "message"
    """
    def _config(self,argv,rargs):
        self.message = ""
        if argv.has_key('-m') :
            self.message = argv['-m']
    def _execute(self,rargs):
        self.loadconf(rargs)
        conf.version.ins().update_ver()
        conf.version.ins().save()
        ver =  conf.version.ins().info()
        conf.git.ins().commit(ver,self.message)
        conf.git.ins().push()

class rc_cmd(dev_cmd_base) :
    """
    提交发布候选(打tag)
    rg rc -m "message"
    """
    def _config(self,argv,rargs):
        self.message = ""
        if argv.has_key('-m') :
            self.message = argv['-m']
    def _execute(self,rargs):
        self.loadconf(rargs)
        conf.version.ins().update_ver()
        conf.version.ins().save()
        ver =  conf.version.ins().info()
        conf.git.ins().commit(ver,self.message)
        conf.git.ins().push()
        conf.git.ins().set_tag(ver)


class sonar_cmd(dev_cmd_base) :
    """
    命令:
    rg sonar

    配置(dev.yaml):
    - !C.sonar
        runner   : "/data/x/tools/sonar/bin/sonar-runner"
        qube     : "http://xxxx"
        src      : "src"
        language : "php"

    """
    def _config(self,argv,rargs):
        pass
    def _execute(self,rargs):
        self.loadconf(rargs)
        conf.sonar.ins().build_file()
        conf.sonar.ins().run()

