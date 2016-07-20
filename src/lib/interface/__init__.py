from  rg_conf import base
from  rg_def  import resource , run_context , controlable , control_box ,control_call, res_proxy
from  rg_err  import *

registed_resource = {}
registed_cmd      = {}
cmds_index        = []
registed_conf     = {}

def regist_res(name,module) :
    name = name.split(',')
    for  res in name:
        registed_resource[res] = module

def regist_cmd(name,module) :
    name = name.split(',')
    for  c in name:
        registed_cmd[c] = module
        cmds_index.append(c) 

def regist_conf(name,module) :
    name = name.split(',')
    for  c in name:
        registed_conf[c] = module
