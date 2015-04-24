#coding=utf-8
import  os , string   , logging ,re ,sys
import  interface,utls.rg_sh

conf_objs = {}
class singleton :
    def _load( self ) :
        key = self.__class__.__name__
        # utls.dbc.must_true(conf_objs.has_key(key), "%s have call _load " %(key))
        self.__init__()
        conf_objs[self.__class__.__name__] = self
        return

    def execmd(self,cmd,check=True, okcode= [0] ,tag = None ):
        utls.rg_sh.shexec.execmd(cmd,check,okcode,tag=self.__class__.__name__)
    @staticmethod
    def get_ins(cls):
        key = cls.__name__
        return conf_objs[key]
