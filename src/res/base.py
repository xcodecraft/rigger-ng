
#coding=utf-8

import  utls.rg_sh

class res_utls:
    def execmd(self,cmd) :
        utls.rg_sh.shexec.execmd(cmd,tag=self.__class__.__name__)
