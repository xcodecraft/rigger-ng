#coding=utf8
import types , re , os , string ,  getopt , pickle , logging
from utls.rg_io import rgio

class rg_cmd:
    def _config(self,argv,rargs):
        pass

    def _execute(self,rargs):
        pass

    def _usage(self):
        if hasattr(self,"__doc__") and self.__doc__ is not None:
            rgio.prompt(str(self.__doc__))
        else:
            rgio.prompt("%s has no more info" % self.__class__)

        pass

class cmdtag_rg :
    pass
class cmdtag_prj :
    pass

class cmdtag_pub :
    pass

