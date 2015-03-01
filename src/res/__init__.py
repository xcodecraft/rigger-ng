from impl.rg_prj import system , project, module , vars , echo , assert_eq

# from mysql import mysql
import impl.rg_prj
import interface

class obj_handler :
    obj = None
def ins_res(name) :
    handler = obj_handler()
    if ins_res_model(name,impl.rg_prj,handler) :
        pass
    # elif    ins_res_model(name,mysql,handler) :
    #     pass
    return handler.obj

def ins_res_model(name,model,handler) :
    reslist = dir(model)
    obj = None
    if name in reslist :
        code = "handler.obj = %s.%s()" %(model.__name__,name)
        exec code
        return True
    return False


for code in interface.load_module_codes :
    exec   code



class control_proxy(interface.resource) :
    def bind_obj(self,obj):
        self.obj = obj
    def _allow(self,context):
        self.obj._allow(context)
        pass
    def _before(self,context):
        self.obj._before(context)
        pass
    def _after(self,context):
        self.obj._after(context)
        pass
    def _start(self,context):
        self.obj._start(context)
        pass
    def _stop(self,context):
        self.obj._stop(context)
        pass
    def _reload(self,context):
        self.obj._reload(context)
        pass
    def _config(self,context):
        self.obj._config(context)
        pass

    def _data(self,context):
        self.obj._data(context)
        pass
    def _check(self,context):
        self.obj._check(context)
        pass
    def _clean(self,context):
        self.obj._clean(context)
        pass

