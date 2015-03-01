#coding=utf8
import re , os , sys,  yaml, logging, time
import interface
# import res.project
import  res
_logger = logging.getLogger()
class conf_loader:
    def  __init__(self,conf):
        self.conf    = conf
        self.curpath = os.path.dirname(self.conf)
        _logger.debug("yaml current path:%s",self.curpath)
    def  replace(self,matchobj):
        filepath = matchobj.groups()[0]
        filepath = re.sub("^\.",self.curpath,filepath)
        filepath = env_exp.value(filepath)
        _logger.debug("import yaml:%s",filepath)
        doc = open(filepath).read()
        return  doc
    def load(self):
        if not os.path.exists(self.conf) :
            raise interface.rigger_exception("unfound file: %s" %self.conf )
        doc = open(self.conf,"r").read()
        doc = re.sub(r"""#!import *["'](.*)["']""",self.replace,doc)
        return doc

    def load_data(self,ori=None,new=None):
        doc = self.load()
        if ori is not None:
            doc = doc.replace(ori,"!!python/object:" + new)
        data = yaml.load(doc)
        return data
