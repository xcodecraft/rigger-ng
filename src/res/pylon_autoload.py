#coding=utf-8
import logging
import interface
import os
import utls.tpl

from utls.rg_io  import rg_logger
from utls.rg_sh  import shexec
from string import *
import sys

_logger = logging.getLogger()

class pylon_autoload(interface.resource):
    """build autoload data for pylon:
       _autoload_clspath.idx
       _autoload_clsname.idx
       _find_cls.tmp
       phpsdk.txt
    """
    def _before(self,context):
        self.src_paths   = self.MODULES.split(':')
    def _config(self,context):
        self.sdk()
        self.build_php_index(self.src_paths,self.sys_autoload,True,"");
    def sdk(self):
        sdk_file   = utls.rg_var.value_of(os.path.join(self.sys_autoload,  "phpsdk.txt"))
        root       = utls.rg_var.value_of(self.root)
        cmd = "find %s -name '*.php' | xargs cat | grep 'require_once' | grep '/home/q/' > %s" %(root, sdk_file)
        shexec.execmd(cmd,False)
    def _clean(self,context):
        pass

    def find_class(self,src,data_file):
        shexec.execmd(Template('echo "" > $DST').substitute(DST=data_file))
        cmdtpl = 'find $SRC/ -name "*.php"   |  xargs  grep  -H -i -E "^ *(abstract)? *class "  >> $DST'
        for  s in src :
            cmd = Template(cmdtpl).substitute( SRC = s ,DST=data_file)
            shexec.execmd(cmd,False)

        cmdtpl = 'find $SRC/ -name "*.php"   |  xargs  grep  -H -i -E "^ *interface "  >> $DST'
        for  s in src :
            cmd = Template(cmdtpl).substitute( SRC =  s ,DST=data_file)
            shexec.execmd(cmd,False)

    def build_php_index(self,src_paths,dst_path,isclear = False,replace=""):
        cls_tmp     = utls.rg_var.value_of(os.path.join(dst_path,  "_find_cls.tmp"))
        out_clspath = utls.rg_var.value_of(os.path.join(dst_path,  "_autoload_clspath.idx"))
        out_clsname = utls.rg_var.value_of(os.path.join(dst_path,  "_autoload_clsname.idx"))
        self.find_class(src_paths,cls_tmp)
        clspath_tmp = utls.rg_var.value_of(os.path.join(dst_path,  "_autoload_clspath.tmp"))
        with   open(clspath_tmp,'w') as autoload :
            with  open(cls_tmp,'r') as find_cls :
                for line in find_cls.readlines():
                    res  =  self.parse_cls(line)
                    if not res :
                        continue
                    file_path=res.group(1)
                    if len(replace) > 0 :
                        file_path= file_path.replace(replace,'')
                    cls =  res.group(3)
                    autoload.write(Template("$CLS,$PATH\n").substitute(PATH=file_path,CLS=cls))
        if isclear :
            shexec.execmd(Template("sort $SRC > $DST; rm $SRC ").substitute(SRC=clspath_tmp,DST=out_clspath))
        else :
            shexec.execmd(Template("sort $SRC >> $DST; rm $SRC ").substitute(SRC=clspath_tmp,DST=out_clspath))

        clsname_tmp = utls.rg_var.value_of(os.path.join(dst_path ,  "_autoload_clsname.tmp"))
        with   open(clsname_tmp,'w') as autoload :
            with  open(cls_tmp,'r') as find_cls :
                for line in find_cls.readlines():
                    res  =  self.parse_cls(line)
                    if not res :
                        continue
                    cls =  res.group(3)
                    autoload.write(Template("cls_$LOWCLS,$CLS\n").substitute(CLS=cls,LOWCLS=cls.lower()))
        if isclear :
            shexec.execmd(Template("sort $SRC > $DST; rm $SRC ").substitute(SRC=clsname_tmp,DST=out_clsname))
        else :
            shexec.execmd(Template("sort $SRC >> $DST; rm $SRC ").substitute(SRC=clsname_tmp,DST=out_clsname))
    def parse_cls(self,line):
        res  = None
        res1 =  re.search('(.*\.php):\s*(abstract)?\s*class\s+(\S+)',line,flags=re.IGNORECASE)
        res2 =  re.search('(.*\.php):\s*(interface)\s+(\S+)',line,flags=re.IGNORECASE)
        if res1 :
            res=res1
        if res2 :
            res= res2
        return res;
