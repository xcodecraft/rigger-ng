#coding=utf8
import types , re , os , string ,  getopt , pickle , logging
from rg_io import rgio

_logger = logging.getLogger()
class rg_cmd:
    def _config(self,argv,rargs):
        pass
        # for o, a in argv.items():
        #     if o == "-v":
        #         rargs.vars_def = a
        #         _logger.info ( "define prior vars : %s " %a)
        #         tpl.tplvar.prior_define(a)
        #     if o == "-u":
        #         rargs.user  = a
        #     if o == "-a" :
        #         rargs.answer = a

    def _execute(self,rargs):
        pass
    def _usage(self):
        if hasattr(self,"__doc__") and self.__doc__ is not None:
            rgio.prompt(str(self.__doc__))
        else:
            rgio.prompt("%s has no more info" % self.__class__)

        pass

# class empty_cmd(rg_cmd):
#     def _execute(self,cmd,rargs):
#         rgio.prompt("Error: '%s' is not a valid rigger command" % cmd)
#     def _usage(self):
#         rgio.prompt("Error: invalid command. type 'rg help' for more info." % self)


class cmdtag_rg :
    pass
class cmdtag_prj :
    pass

class cmdtag_pub :
    pass

