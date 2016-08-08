#coding=utf-8
import logging
import interface

from utls.rg_io  import rgio,rg_logger
from utls.rg_var import value_of
from utls.rg_sh  import shexec
from impl.rg_utls  import *
from res.base   import *
from utls.rg_sh  import shexec
from shared_utls import *



class nginx_conf_base(interface.resource):

    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.bin           = res_utls.value(self.bin)
            self.name          = res_utls.value(self.name)
            self.dst           = res_utls.value(self.dst) + self.name
            self.src           = res_utls.value(self.src)
            self.src           = tpldst_path(self.tpl,self.src)
            self.tpl           = res_utls.value(self.tpl)
            self.testbin       = res_utls.value(self.testbin)

            self.tpl_res       = res.file_tpl()
            self.tpl_res.sudo  = self.sudo
            self.tpl_res.tpl   = self.tpl
            self.tpl_res.dst   = self.src
            self.tpl_res._before(context)

            self.link_res      = res.link()
            self.link_res.sudo = self.sudo
            self.link_res.dst  = self.dst
            self.link_res.src  = self.src
            self.link_res._before(context)

    def _after(self,context):
        self.link_res._after(context)
        self.tpl_res._after(context)
        pass

    def _config(self,context) :
        self.tpl_res._config(context)
        self.link_res._config(context)
        cmdtpl = "$BIN -t"
        cmd = Template(cmdtpl).substitute(
                BIN = self.testbin
                )
        shexec.execmd(cmd)
        pass

    def _start(self,context) :
        self._reload(context)
    def _clean(self,context) :
        self.link_res._clean(context)
        self.tpl_res._clean(context)

    def _reload(self,context) :
        self.tpl_res._reload(context)
        self.link_res._reload(context)

        cmdtpl = "$BIN reload"
        cmd = Template(cmdtpl).substitute(
                BIN = self.bin
                )
        shexec.execmd(cmd)
