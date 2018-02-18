#coding=utf8
import re,logging
import interface,utls.rg_var,utls.rg_json
import utls.dbc , utls.check
import copy
from utls.rg_io import  rgio , run_struct,rg_logger
from utls.tpl.tpl_var import safe_env_porp
from impl.rg_utls import *
from utls.rg_sh  import shexec
import hashlib

from utls.rg_var import value_of
from impl.rg_utls import *
from res.base   import *

def cacu_file_sha(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.sha256()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    hash_code = myhash.hexdigest()
    f.close()
    return str(hash_code).lower()


def have_cmd(expect,dst) :
    arr = dst.split(',')
    for i in arr :
        if i.strip()  == expect.strip() :
            return True
    return False
class assert_file_sha(interface.resource,res_utls) :
    """
    sha use sha256, centos: sha256sum
    !R.assert_file_sha
    file  : ""
    sha   : ""
    run   : "check"  "check,conf,start"
    """
    name = "assert_file_sha"
    run  = "check"

    def _allow(self,context):
        return True
    def _config(self,context):
        if have_cmd('conf',self.run) :
            self.assert_sha(context)
    def assert_sha(self,context,is_raise = True):
        dst        = res_utls.value(self.file)
        sha        = res_utls.value(self.sha)
        dst_sha    = cacu_file_sha(dst)
        if sha != dst_sha:
            if is_raise :
                raise interface.rigger_exception("file MD5: %s , expect MD5 : %s " %(dst_sha,sha))
            return False
        return True
    def _start(self,context) :
        if have_cmd('start',self.run) :
            self.assert_sha(context)

    def _check(self,context):
        if have_cmd('check',self.run) :
            result = self.assert_sha(context,False)
            self._check_print(result,self.file)


class assert_url_sha(interface.resource,res_utls) :
    """
    sha use sha256, centos: sha256sum
    !R.assert_file_sha
    url  : ""
    head  : ""
    sha   : ""
    run   : "check"  "check,conf,start"
    """
    name = "assert_url_sha"
    head = ""
    run  = "check"

    def _allow(self,context):
        return True
    def _config(self,context):
        if have_cmd('conf',self.run) :
            self.do_curl(context)
            self.assert_sha(context)

    def do_curl(self,context) :
        self.head = res_utls.value(self.head)
        self.file = context.run_path + "/curl_out.data"
        cmd = "curl -q \"$URL\" -X GET > $OUT"
        shexec.execmd(Template(cmd).substitute(URL=self.url,OUT=self.file))

    def assert_sha(self,context,is_raise=True):
        sha        = res_utls.value(self.sha)
        dst_sha    = cacu_file_sha(self.file)
        if sha != dst_sha:
            if is_raise :
                raise interface.rigger_exception("url content SHA: %s , expect SHA : %s " %(dst_sha,sha))
            return False ;
        return True
    def _start(self,context) :
        if have_cmd('start',self.run) :
            self.do_curl(context)
            self.assert_sha(context)

    def _check(self,context):
        if have_cmd('check',self.run) :
            self.do_curl(context)
            result = self.assert_sha(context,False)
            self._check_print(result,self.url)
