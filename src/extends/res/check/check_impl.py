#coding=utf8
import re,logging
import interface,utls.rg_var,utls.rg_json
import utls.dbc , utls.check
import copy
from utls.rg_io import  rgio , run_struct,rg_logger
from utls.tpl.tpl_var import safe_env_porp
from impl.rg_utls import *
import hashlib

from utls.rg_var import value_of
from impl.rg_utls import *
from res.base   import *

def cacu_file_md5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
        f.close()
        return myhash.hexdigest()

class assert_file_md5(interface.resource,res_utls) :
    """
    !R.assert_file_md5
    file  : ""
    md5   : ""
    """
    name = "assert_file_md5"

    def _allow(self,context):
        return True
    def _config(self,context):
        self.assert_md5(context)
    def assert_md5(self,context):
        dst        = res_utls.value(self.file)
        md5        = res_utls.value(self.md5)
        dst_md5    = cacu_file_md5(dst)
        if md5 != dst_md5:
            raise interface.rigger_exception("file MD5: %s , expect MD5 : %s " %(dst_md5,md5))
    def _start(self,context) :
        self.assert_md5(context)
