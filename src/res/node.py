#coding=utf8
import  utls.tpl ,utls.rg_var,interface
import  utls.rg_yaml
import  res

data_files = []

mod_objs = {}
env_objs = {}
sys_objs = {}

def module_regist(modul):
    mod_objs[modul._name] = modul

def module_find(name):
    if mod_objs.has_key(name) :
        return mod_objs[name]
    return None

def env_regist(obj):
    env_objs[obj._name] = obj

def env_find(name):
    if env_objs.has_key(name) :
        return env_objs[name]
    return None

def sys_regist(obj):
    sys_objs[obj._name] = obj

def sys_find(name):
    if sys_objs.has_key(name) :
        return sys_objs[name]
    return None

def module_load(fname) :
    if fname in data_files :
        return
    data_files.append(fname)
    loader = utls.rg_yaml.conf_loader(fname)
    data   = loader.load_data("!R","res")
    if data.has_key('_mod') :
        for m in  data['_mod'] :
            module_regist(m)
