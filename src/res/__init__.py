from impl.rg_framework import system , project, module , vars , echo , assert_eq

def ins_res(name) :
    import impl.rg_framework
    reslist = dir(impl.rg_framework)
    if name in reslist :
        exec "obj = impl.rg_framework.%s()" %name
        return obj
    return None


