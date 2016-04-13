#coding=utf-8
import os,re,logging
import interface
import utls.pattern
import utls.dbc
import copy

from utls.rg_io import  rg_logger

def upper_dict(ori) :
    # utls.dbc.must_true(isinstance(ori,dict)," upper_dict need porp obj, %s" %(ori.__class__.__name__) )
    now = {}
    for k,v in ori.items() :
        nkey = k.upper()
        now[nkey] = v
    return now


class porp :
    def set(self,name,val) :
        raise interface.rigger_exception(" %s no impl set methond " %self.__class__.__name__)
    def get(self,name) :
        raise interface.rigger_exception(" %s no impl get methond " %self.__class__.__name__)

class attr_proxy(porp) :
    def __init__(self,p) :
        utls.dbc.must_obj(p,porp)
        self.__dict__['impl'] = p
    def __getattr__(self,name):
        return self.__dict__['impl'].get(name)
    def get(self,name):
        return self.__dict__['impl'].get(name)

    def __setattr__(self,name,val):
        return self.__dict__['impl'].set(name,val)

    def set(self,name,val):
        return self.__dict__['impl'].set(name,val)

class porp_proxy(porp):
    def __init__(self,p) :
        self.impl = p
    def get(self,name):
        return getattr(self.impl,name)
    def set(self,name,val):
        return setattr(self.impl,name,val)

class icase_porp(porp) :
    def __init__(self) :
        self._iattrs = {}
    def set(self,name,val) :
        self._iattrs[name.upper()] = val

    def get(self,name) :
        name = name.upper()
        if  self._iattrs.has_key(name) :
            return  self._iattrs[name]
        return None

class empty_porp(porp):
    def get(self,name):
        # import pdb
        # pdb.set_trace()
        raise interface.var_undefine("undefined value [%s]!" %name)
    def export(self,target) :
        pass

class dict_porp(icase_porp):
    def __init__(self,dict_obj) :
        self._iattrs = {}
        self._iattrs.update(upper_dict(dict_obj))

    def export(self,target) :
        target.update(self._iattrs)



class  safe_env_porp(icase_porp) :
    _ins = None
    @staticmethod
    def ins():
        if safe_env_porp._ins is None :
            safe_env_porp._ins = safe_env_porp()
        return  safe_env_porp._ins
    def __init__(self) :
        self.update(['HOME','USER','PRJ_ROOT'])
    def update(self,keys) :
        self._iattrs = {}
        for i in keys :
            if os.environ.has_key(i) :
                self._iattrs[i] = os.environ[i]
    def export(self,target) :
        target.update(self._iattrs)

class combo_porp(porp) :
    def __init__(self,first,second):
        utls.dbc.must_obj(first,porp)
        utls.dbc.must_obj(second,porp)
        self._first  = first
        self._second = second

    def get(self,name):
        val =     self._first.get(name)
        if  val is None :
            return self._second.get(name)
        return val
    def export(self,target) :
        # 反序
        self._second.export(target)
        self._first.export(target)



class layzer_porp(icase_porp):
    def __init__(self,var_funs={},default_fun=None):
        icase_porp.__init__(self)
        self._var_funs    = upper_dict(var_funs)
        self._default_fun = default_fun

    def get(self,name):
        name = name.upper()
        val  = icase_porp.get(self,name)
        if val is not None :
            return val

        fun  = self._default_fun
        if  self._var_funs.has_key(name) :
            fun = self._var_funs[name]

        if fun is None :
            raise interface.rigger_exception(" layzer_porp   %s no fun" %name)
        val = fun(name)
        if val is None :
            raise interface.rigger_exception(" layzer_porp   %s is None" %name)
        self.set(name,val)
        return val


def parse_assign(defstr):
    """x=1,y=2 """
    res={}
    for ass  in defstr.split(','):
        match = re.match(r'(\w+)=(.+)',ass)
        if match:

            key = match.group(1).strip()
            val = match.group(2).strip()
            rg_logger.debug( "parse %s:%s " %(key,val))
            res[key]=val
    return res


