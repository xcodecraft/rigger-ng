#coding=utf8
import  logging
from base.tc_tools   import *
import  utls.tpl
import  interface
import  utls.rg_json
from utls.rg_var_impl import *

class json_tc(rigger_tc) :
    def test_json(self) :
        jfile = os.path.dirname(os.path.dirname(__file__)) + "/data/data.json"
        data =  utls.rg_json.load_file(jfile,"/env/dev")
        expect = {u'DB_USER': u'rigger', u'DB_NAME': u'127.0.0.1'}
        self.assertEqual(data,expect)
    def test_badjson(self) :
        try:
            jfile = os.path.dirname(os.path.dirname(__file__)) + "/data/bad.json"
            data =  utls.rg_json.load_file(jfile,"/env/dev")
        except interface.rigger_exception :
            pass
    def test_nojson(self) :
        try :
            jfile = os.path.dirname(os.path.dirname(__file__)) + "/data/bad1.json"
            data =  utls.rg_json.load_file(jfile,"/env/dev")
        except interface.rigger_exception:
            pass
