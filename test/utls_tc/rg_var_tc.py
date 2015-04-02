#coding=utf8
import  logging
from base.tc_tools   import *
import  utls.tpl
import  interface
from utls.rg_var_impl import *

class tplvar_tc(rigger_tc) :
    def test_tplvar(self) :
        var = rgvar_god()
        var.import_str("a=x")
        var.import_str("b=y,c=z")

        attr_val = attr_proxy(var.current())
        self.assertEqual(attr_val.a, 'x')
        self.assertEqual(attr_val.b, 'y')
        self.assertEqual(attr_val.c, 'z')

        var.keep()
        var.import_str("a=x1,b=y1,c=z1")
        attr_val = attr_proxy(var.current())
        self.assertEqual(attr_val.a, 'x1')
        self.assertEqual(attr_val.b, 'y1')
        self.assertEqual(attr_val.c, 'z1')

        var.rollback()
        attr_val = attr_proxy(var.current())
        self.assertEqual(attr_val.a, 'x')
        self.assertEqual(attr_val.b, 'y')
        self.assertEqual(attr_val.c, 'z')
