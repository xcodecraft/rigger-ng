#coding=utf-8
import logging
import interface
import os ,re
import utls.tpl

from utls.rg_io  import rg_logger
from utls.rg_sh  import shexec
from string import *
from res.base   import *
import sys

_logger = logging.getLogger()

class pylon_autoload(interface.resource,res_utls):
    """build autoload data for pylon:
    !R.pylon_autoload :
        inlcude :  "/home/x/php:/usr/local/php/lib"
        dst     :  "${RUN_PATH}/autoload"
    """
    sdk_base = "/home/"
    include  = ""
    dst      = "${RUN_PATH}/autoload"
    def _before(self,context):
        # self.sdk_file  = self.dst_path("phpsdk.txt")
        self.include   = res_utls.value( self.include)
        self.dst       = res_utls.value(self.dst)
        if not os.path.exists(self.dst) :
            os.makedirs(self.dst)

    def _config(self,context):
        src_paths = self.include.split(':')
        self.build_php_index(src_paths,self.dst,True,"");

    def dst_path(self,filename) :
        abs_path  = res_utls.value(os.path.join(self.dst,  filename))
        return  abs_path
    # def build_sdk(self):
    #     root       = utls.rg_var.value_of(self.root)
    #     sdk_filter = "grep 'require' | grep '%s' " %(self.sdk_base)
    #     cmd        = "find %s -name '*.php' | xargs cat | %s  > %s" %(root, sdk_filter,self.sdk_file)
    #     shexec.execmd(cmd,False)
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
        # import pdb
        # pdb.set_trace()
        cls_tmp     = self.dst_path( "_find_cls.tmp")
        out_clspath = self.dst_path( "_autoload_clspath.idx")
        out_clsname = self.dst_path( "_autoload_clsname.idx")
        self.find_class(src_paths,cls_tmp)
        clspath_tmp = self.dst_path( "_autoload_clspath.tmp")
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

class pylon_router(interface.resource,res_utls):
    """
    !R.pylon_router
        include: "$${PRJ_ROOT}/src/apps/api"
    """
    include = ""
    dst     = "${RUN_PATH}/router/"
    def _before(self,context):
        self.include = res_utls.value(self.include)
        self.dst     = res_utls.value(self.dst)
        res_utls.ensure_path(self.dst)
        self.out_idx = os.path.join(self.dst , "_router.idx")

    def _config(self,context):

        sed     = """sed -r "s/.+:class\s+(\S+)\s+.+\/\/\@REST_RULE:\s+(.+)/\\2 : \\1/g" """
        cmdtpl  = """grep --include "*.php" -i  -E "class .+ implements XService"  -R $SRC   |  """  + sed + " > $DST "
        cmd     = Template(cmdtpl).substitute(SRC = self.include,DST = self.out_idx)
        shexec.execmd(cmd,False)

    def _check(self,context):
        self.check_print(os.path.exists(self.out_idx),self.out_idx)

    def clean_file(self,filename):
        cmdtpl = "if test -e $DST ; then rm -f  $DST ; fi ; "
        cmd    = Template(cmdtpl).substitute(DST=filename)
        shexec.execmd(cmd)

    def _clean(self,context):
        self.clean_file(self.out_idx)

