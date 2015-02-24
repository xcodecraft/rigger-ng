#coding=utf-8
import interface
import tc_tools

from impl.rg_yaml  import *
class yaml_conf_tc(tc_tools.rigger_tc):
    def test_resyaml(self):
        # print("--------")
        # a = res.project()
        # print(a._resname())

        loader = conf_loader("/Users/pylon/devspace/rigger-ng/test/data/res_v2.yaml")
        data   = loader.load_data("!R","res")
        print(data['__prj'].name)
        print(data['__sys'][0].name)
