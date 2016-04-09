#coding=utf8
import types , re , os , string ,  getopt , pickle , logging
from utls.rg_io import rgio

class rg_cmd:
    def _config(self,argv,rargs):
        pass

    def _execute(self,rargs):
        pass

    def useage(self,output):
        if hasattr(self,"__doc__") and self.__doc__ is not None:
            output(str(self.__doc__))
        else:
            output("%s has no more info" % self.__class__)

class cmdtag_rg :
    pass
class cmdtag_prj :
    pass

class cmdtag_pub :
    pass

