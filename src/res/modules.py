#coding=utf8
import  utls.tpl ,utls.rg_var,interface
import  impl.rg_yaml
import  res

modules = {}
data_files = []
def regist(modul):
    modules[modul._name] = modul

def find(name):
    if modules.has_key(name) :
        return modules[name]
    return None

def load(fname) :
    if fname in data_files :
        return
    loader = impl.rg_yaml.conf_loader(fname)
    data_files.append(fname)
    data   = loader.load_data("!R","res")
    if data.has_key('_mod') :
        for m in  data['_mod'] :
            regist(m)
