from impl.rg_prj import system , project, module , vars , echo , assert_eq

from mysql import mysql
import impl.rg_prj

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

