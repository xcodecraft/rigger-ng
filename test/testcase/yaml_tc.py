#coding=utf-8
import interface
import tc_tools

from impl.rg_yaml  import *
import impl.rg_var
class yaml_conf_tc(tc_tools.rigger_tc):
    def test_resyaml(self):

        root   = impl.rg_var.value_of("${HOME}/devspace/rigger-ng")
        loader = conf_loader( root + "/test/data/res_v2.yaml")
        data   = loader.load_data("!R","res")
        # print(data['__prj'].name)
        # print(data['__sys'][0].name)
