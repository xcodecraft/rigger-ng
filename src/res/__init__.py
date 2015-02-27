from impl.rg_prj import system , project, module , vars , echo , assert_eq

def ins_res(name) :
    import impl.rg_prj
    reslist = dir(impl.rg_prj)
    if name in reslist :
        exec "obj = impl.rg_prj.%s()" %name
        return obj
    return None


