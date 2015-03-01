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

class controlable :
    def _allow(self,context):
        pass

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

load_module_codes= []
def load_res(code) :
    load_module_codes.append(code)

def control_call(res,fun,context) :
    import  utls.rg_sh
    # with rg_io.scope_iotag(res._resname(),name,res._info()) :
        # if res._allow(context) :
    # with utls.rg_sh.scope_sudo(res.sudo) :
    res._before(context)
    fun(res,context)
    res._after(context)

class control_box(controlable):

    def __init__(self):
        self.res = []

    def items_call(self,fun,context):
        if self._allow(context):
            for r in self.res :
                control_call(r,fun,context)

    def _start(self,context):
        self.items_call(rg_model.res_runner.start,context)

    def _stop(self,context):
        self.items_call(rg_model.res_runner.stop,context)

    def _config(self,context):
        self.items_call(controlable._config,context)
    def _data(self,context):
        self.items_call(rg_model.res_runner.data,context)
    def _check(self,context):
        self.items_call(rg_model.res_runner.check,context)

    def _reload(self,context):
        self.items_call(rg_model.res_runner.reload,context)
    def _clean(self,context):
        self.items_call(rg_model.res_runner.clean,context)
    def _allow(self,context):
        return True
    def append(self,item):
        self.res.append(item)
    def push(self,item):
        self.res.insert(0,item)

class resource (controlable,rg_conf.base):
    sudo        = False
    allow_res   = "ALL"

    def _allow(self,context):
        allowd =  self.allow_res == "ALL"  or self.allow_res == self.clsname()
        if allowd:
            _logger.debug( "allowd resource %s ,current resouce is %s " %(self.allow_res,self._clsname()))
        return  allowd

    def _check_print(self,is_true,msg):
        if is_true:
            print( "%-100.100s%-20.20s-[Y]" % (msg ,self.clsname())  )
        else:
            print( "%-100.100s%-20.20s-[ ]" % (msg ,self.clsname())  )
    def _resname(self):
        tag = self.__class__.__name__
        return tag
    def _info(self):
        return ""

class empty_res(resource):
    def useage(self,output):
        output("no found this res")

