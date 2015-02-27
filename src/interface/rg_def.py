#coding=utf-8
import logging
import rg_conf
_logger = logging.getLogger()

class run_context :
    def __init__(self):
        self.restore = None
    def keep(self) :
        import copy
        self.restore =  copy.copy(self.__dict__)
    def rollback(self):
        import copy
        self.__dict__=  copy.copy(self.restore)
        self.restore = None

class resource (rg_conf.base):
    sudo        = False
    allow_res   = "ALL"

    def _allow(self,context):
        allowd =  self.allow_res == "ALL"  or self.allow_res == self.clsname()
        if allowd:
            _logger.debug( "allowd resource %s ,current resouce is %s " %(self.allow_res,self._clsname()))
        return  allowd

    def _before(self,context):
        pass
    def _after(self,context):
        pass
    def _start(self,context):
        pass
    def _stop(self,context):
        pass
    def _reload(self,context):
        pass
    def _config(self,context):
        pass

    def _data(self,context):
        pass
    def _check(self,context):
        pass
    def _clean(self,context):
        pass
    def _clsname(self):
        return self.__class__.__name__
    def _check_print(self,is_true,msg):
        if is_true:
            print( "%-100.100s%-20.20s-[Y]" % (msg ,self.clsname())  )
        else:
            print( "%-100.100s%-20.20s-[ ]" % (msg ,self.clsname())  )
    def _resname(self):
        tag = self._clsname()
        return tag
    def _info(self):
        return ""

class empty_res(resource):
    def useage(self,output):
        output("no found this res")

