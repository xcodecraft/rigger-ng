#coding=utf8
from utls.rg_io import rgio , rg_logger
import interface
import utls.rg_var , utls.dbc , utls.check
import res.node
import os


def check_data(data):
    utls.check.not_none(data ,"project no yaml data")
    # utls.check.must_true(data.has_key('_env'),"project no _env data")
    # utls.check.must_true(data.has_key('_sys'),"project no _sys data")
    return True

def load(conf_yaml) :
    import utls.rg_yaml,copy
    rg_logger.info("load prj conf: %s" %(conf_yaml))
    loader = utls.rg_yaml.conf_loader(conf_yaml)
    data   = loader.load_data("!R","res")
    # print("-------------%s----------" %(conf_yaml))
    check_data(data)


    if data.has_key('_mod') :
        for m  in  data['_mod'] :
            res.node.module_regist(m)

    if data.has_key('_env') :
        for obj  in data['_env']:
            res.node.env_regist(obj)

    if data.has_key('_sys') :
        for obj  in data['_sys']:
            res.node.sys_regist(obj)
