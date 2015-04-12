
#coding=utf-8

import  utls.rg_sh
import  utls.rg_var
import  os

class res_utls:
    def execmd(self,cmd) :
        utls.rg_sh.shexec.execmd(cmd,tag=self.__class__.__name__)

    @staticmethod
    def value(v) :
        nv =   utls.rg_var.value_of(v)
        return nv

    @staticmethod
    def ensure_path(dst) :
        dst       = res_utls.value(dst)
        if not os.path.exists(dst) :
            os.makedirs(dst)

