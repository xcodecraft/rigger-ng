#coding=utf8
import re , os , yaml, logging
import interface
import utls.dbc
from utls.rg_io import rg_logger


class conf_loader:
    def  __init__(self,conf):
        self.conf    = conf
        utls.dbc.must_exists(self.conf)
        self.curpath = os.path.dirname(self.conf)
        rg_logger.debug("yaml current path:%s" %self.curpath)
    def  replace(self,matchobj):
        filepath = matchobj.groups()[0]
        filepath = re.sub("^\.",self.curpath,filepath)
        filepath = env_exp.value(filepath)
        rg_logger.debug("import yaml:%s",filepath)
        doc      = open(filepath).read()
        return  doc
    def load(self):
        utls.dbc.must_file(self.conf)
        doc = open(self.conf,"r").read()
        doc = re.sub(r"""#!import *["'](.*)["']""",self.replace,doc)
        return doc

    def load_data(self,ori=None,new=None):
        doc = self.load()
        if ori is not None:
            doc = doc.replace(ori,"!!python/object:" + new)
        data = yaml.load(doc)
        return data
