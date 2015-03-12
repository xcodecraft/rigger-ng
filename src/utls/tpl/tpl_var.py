#coding=utf-8
import os,re,logging
import interface
import utls.pattern
import utls.dbc


_logger = logging.getLogger()

class porp :
    pass


class empty_porp(porp):
    def __getattr__(self,name):
        raise interface.var_undefine("undefined value [%s]!" %name)
    pass

class dict_porp(porp ):
    def __init__(self,dict_obj) :
        self.__dict__.update(dict_obj)

class combo_porp(porp):
    def __init__(self,first,second):
        self._first  = first
        self._second = second

    def __getattr__(self,name):
        # if name == "PRJ_NAME " :
        #     import pdb
        #     pdb.set_trace()
        if hasattr(self._first,name):
            return getattr(self._first,name)
        else :
            return getattr(self._second,name)



class layzer_porp(porp):
    def __init__(self,var_funs={},default_fun=None):
        self._var_funs    = var_funs
        self._default_fun = default_fun

    def __getattr__(self,name):
        # import pdb
        # pdb.set_trace()
        fun = self._default_fun
        if  self._var_funs.has_key(name) :
            fun = self._var_funs[name]
        if fun is None :
            return None
        val = fun.execute(name)
        if val is None :
            raise interface.rigger_exception(" layzer_porp   %s is None" %name)
        # not need call fun again!
        setattr(self,name,val)
        return val


def parse_assgin(defstr):
    """x=1,y=2 """
    res={}
    for ass  in defstr.split(','):
        match = re.match(r'(\w+)=(.+)',ass)
        if match:

            key = match.group(1).strip()
            val = match.group(2).strip()
            _logger.debug( "parse %s:%s " %(key,val))
            res[key]=val
    return res

def upper_dict(ori) :
    utls.dbc.must_true(isinstance(ori,dict)," upper_dict need porp obj" )
    now = {}
    for k,v in ori.items() :
        nkey = k.upper()
        now[nkey] = v
    return now

class tpl_var(utls.pattern.singleton):
    def __init__(self):
        self.impl     = combo_porp(dict_porp(os.environ),empty_porp())
        self.restores = []

    def import_dict(self,dict_obj):
        utls.dbc.must_true(isinstance(dict_obj,dict)," tpl_var.import_dict need dict obj" )
        dict_obj  = upper_dict(dict_obj)
        self.impl = combo_porp(dict_porp(dict_obj),self.impl)

    def import_porp(self,porpobj) :
        self.impl = combo_porp(porpobj,self.impl)

    def import_str(self,asstr):
        dict_obj  = parse_assgin(asstr)
        # import pdb
        # pdb.set_trace()
        self.impl = combo_porp(dict_porp(dict_obj),self.impl)

    def clean(self):
        self.__init__()
    def keep(self) :
        import  copy
        self.restores.append( copy.copy(self.impl))
    def rollback(self) :
        self.impl = self.restores.pop()


var = tpl_var()

def var_obj():
    return var.impl

def undefine_value(key):
    return "__NOFOUND_[%s]__" %key


class scope_using:
    def __init__(self,new):
        self.using = new
    def __enter__(self):
        var.keep()
        var.import_porp(self.using)
    def __exit__(self,exc_type,exc_value,traceback):
        var.rollback()
