#coding=utf-8
import os,re,logging
import interface
import utls.pattern


_logger = logging.getLogger()

class prompt_dict:
    def __init__(self,data=None):
        self.data = data
    def __getattr__(self,name):
        # rgio.error("undefined value [%s]!" %name)
        if self.data is not None:
            recommend = prompt.recommend(name,self.data.keys())
            # rgio.error("å¯è½æ¯%s: " %recommend)
        return "__NOFOUND_[%s]__" %name

class empty_dict:
    def __getattr__(self,name):
        raise interface.var_undefine("undefined value [%s]!" %name)
    pass

class prior_dict:
    def __init__(self,ori,prior):
        self.__dict__['_ori']    = ori
        self.__dict__['_prior']  = prior

    def prior_assin(self,name,val):
        prior = self.__dict__['_prior']
        prior[name] = val
    def __setattr__(self,name,val):
        ori   = self.__dict__['_ori']
        setattr(ori,name,val)
    def ori(self):
        return self.__dict__['_ori']
    def set_ori(self,v):
        self.__dict__['_ori'] =v
    def set_oris(self,oris):
        for k,v in oris.items():
            self.__dict__[k] = v
    def __getattr__(self,name):
        prior = self.__dict__['_prior']
        ori   = self.__dict__['_ori']
        name  = name.upper()
        if prior.has_key(name):
            return prior[name]
        else:
            return getattr(ori,name)


class layzer_var:
    def __init__(self,var_funs={},default_fun=None):
        ivar_funs = {}
        for k,v in var_funs.items() :
            ivar_funs[k.upper()] = v
        self.__dict__['_var_funs']    = ivar_funs
        self.__dict__['_default_fun'] = default_fun
    def __getattr__(self,name):
        if  self.__dict__['_var_funs'].has_key(name) :
            v = self.__dict__['_var_funs'][name].execute(name)
        else:
            fun = self.__dict__['_default_fun']
            if fun is not None:
                v = fun.execute(name)
        if v is  None :
            return None
        self.__dict__[name] =  v
        return v


def parse_assgin(defstr):
    """x=1,y=2 """
    res={}
    for ass  in defstr.split(','):
        match = re.match(r'(\w+)=(.+)',ass)
        if match:

            key = match.group(1).strip().upper()
            val = match.group(2).strip()
            _logger.debug( "parse %s:%s " %(key,val))
            res[key]=val
    return res

def upper_dict(ori) :
    now = {}
    for k,v in ori.items() :
        nkey = k.upper()
        now[nkey] = v
    return now

class tpl_var(utls.pattern.singleton):
    def __init__(self):
        self.impl    = prior_dict(empty_dict(),os.environ)
        self.restore = None
        # self.base = self.impl

    def import_dict(self,def_dict):
        def_dict = upper_dict(def_dict)
        self.impl = prior_dict(self.impl,def_dict)

    def import_str(self,asstr):
        def_dict  = parse_assgin(asstr)
        self.impl = prior_dict( self.impl,def_dict)
    def dict(self):
        return self.impl

    def clean(self):
        self.__init__()
    def keep(self) :
        import  copy
        self.restore = copy.copy(self.impl)
    def rollback(self) :
        self.impl = self.restore


var = tpl_var()

def undefine_value(key):
    return "__NOFOUND_[%s]__" %key
    # nofound  = prompt_dict(os.environ)
    # return getattr(nofound,key)


# class scope_nofound:
#     def __init__(self,new):
#         self.nofound = new
#     def __enter__(self):
#         self.ori       = tpl_var.ins().base.ori()
#         tpl_var.ins().base.set_ori(self.nofound)
#     def __exit__(self,exc_type,exc_value,traceback):
#         tpl_var.ins().base.set_ori(self.ori)
