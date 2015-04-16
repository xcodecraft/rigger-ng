#coding=utf-8
import logging
import interface

from utls.rg_io  import rg_logger
from utls.rg_var import value_of
from utls.rg_sh  import shexec
from impl.rg_utls  import *
from res.base   import *
from utls.rg_sh  import shexec


class nginx_conf(interface.resource):
    """
    !R.nginx_conf
        port:       "80"
        http_ip:    "0.0.0.0"
        admin_port: "2000"
        admin_ip:   "127.0.0.1"
        mem:        "20M"
        vcl:        "${PRJ_ROOT}/conf/used/local_cache.vcl"
        name:       "local_proxy_${ENV}"
        extras:     "-w 100,1000,60"
    """

    dst        = "i/etc/nginx/sites-enable/default"
    src        = "${PRJ_ROOT}/conf/used/nginx.conf"
    tpl        = "${PRJ_ROOT}/conf/option/nginx.conf"


    def _before(self,context):
        self.dst =  res_utls.value(self.dst)
        self.src =  res_utls.value(self.src)
        self.tpl =  res_utls.value(self.tpl)

        self.tpl_res      = res.file_tpl()
        self.tpl_res.tpl  = self.tpl
        self.tpl_res.dst  = self.src
        self.tpl_res._before(context)

        self.link_res     = res.link()
        self.link_res.dst = self.dst
        self.link_res.src = self.dst
        self.link_res._before(context)

    def _after(self,context):
        self.link_res._after(context)
        self.tpl_res._after(context)
        pass

    def _config(self,context) :
        self.tpl_res._config(context)
        self.link_res._config(context)
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
                BIN = context.nginx_def.bin
                )
        shexec.execmd(cmd)
