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

from  pylon.parser import  php_class_parser,php_rest_parser

_logger = logging.getLogger()



class pylon_autoload(interface.resource,res_utls):
    """build autoload data for pylon:
    !R.pylon_autoload :
        inlcude :  "/home/x/php:/usr/local/php/lib"
        dst     :  "${RUN_PATH}/autoload"
    """
    include  = ""
    relpath  = ""
    dst      = "${RUN_PATH}/autoload"
    def _before(self,context):
        # self.sdk_file  = self.dst_path("phpsdk.txt")
        self.include   = res_utls.value( self.include)
        self.relpath   = res_utls.value( self.relpath)
        self.dst       = res_utls.value(self.dst)

    def _config(self,context):

        if not os.path.exists(self.dst) :
            os.makedirs(self.dst)
        src_paths = self.include.split(':')
        isfirst   = True

        out_clspath = self.dst_path( "_autoload_clspath.idx")
        out_clsname = self.dst_path( "_autoload_clsname.idx")
        clspath_tmp = self.dst_path( "_autoload_clspath.tmp")
        clsname_tmp = self.dst_path( "_autoload_clsname.tmp")

        with   open(clspath_tmp,'w') as clspath_index  :
            with open(clsname_tmp,'w') as clsname_index :
                for src in  src_paths :
                    if len(src.strip()) == 0 :
                        continue
                    self.build_php_index(src,clspath_index,clsname_index,self.relpath);

        shexec.execmd(Template("sort $SRC > $DST; rm $SRC ").substitute(SRC=clspath_tmp,DST=out_clspath))
        shexec.execmd(Template("sort $SRC > $DST; rm $SRC ").substitute(SRC=clsname_tmp,DST=out_clsname))

    def dst_path(self,filename) :
        abs_path  = res_utls.value(os.path.join(self.dst,  filename))
        return  abs_path

    def _clean(self,context):
        pass

    def find_php(self,src,data_file):
        shexec.execmd(Template('echo "" > $DST').substitute(DST=data_file))
        cmd = Template('find $SRC/ -name "*.php"  >> $DST').substitute( SRC = src ,DST=data_file)
        shexec.execmd(cmd,False)

    def build_php_index(self,src_paths,clspath_index,clsname_index,replace=""):
        # import pdb
        # pdb.set_trace()
        cls_tmp     = self.dst_path( "_find_cls.tmp")
        self.find_php(src_paths,cls_tmp)
        with  open(cls_tmp,'r') as find_cls :
            for line in find_cls.readlines():
                line = line.strip()
                if not os.path.exists(line) :
                    continue
                if os.path.isfile(line) :
                    parser = php_class_parser()
                    parser.parse_file(line,replace,clspath_index,clsname_index)


class pylon_router(interface.resource,res_utls):
    """
    !R.pylon_router
        include: "$${PRJ_ROOT}/src/apps/api:$${PRJ_ROOT}/src/apps/1"
        version: 1
    """
    include = ""
    version = 1
    dst     = "${RUN_PATH}/router/"
    def _before(self,context):
        self.include = res_utls.value(self.include)
        self.dst     = res_utls.value(self.dst)
        res_utls.ensure_path(self.dst)
        self.out_idx = self.dst_path( "_router.idx")

    def find_php(self,src,data_file):
        shexec.execmd(Template('echo "" > $DST').substitute(DST=data_file))
        cmd = Template('find $SRC/ -name "*.php"  >> $DST').substitute( SRC = src ,DST=data_file)
        shexec.execmd(cmd,False)

    def dst_path(self,filename) :
        abs_path  = res_utls.value(os.path.join(self.dst,  filename))
        return  abs_path

    def build_rest_index(self,src_paths,dst_fobj):
        php_files   = self.dst_path( "_php_cls.tmp")
        self.find_php(src_paths,php_files)
        with  open(php_files,'r') as phps_fobj:
            for line in phps_fobj.readlines():
                line = line.strip()
                if not os.path.exists(line) :
                    continue
                parser = php_rest_parser()
                parser.parse_file(line,dst_fobj,self.version)



    def _config(self,context):
        src_paths   = self.include.split(':')
        router_tmp  = self.dst_path( "_router.tmp")
        with open(router_tmp,'w') as router_fobj:
            for src in  src_paths :
                self.build_rest_index(src,router_fobj);
        shexec.execmd(Template("sort $SRC > $DST; rm $SRC ").substitute(SRC=router_tmp,DST=self.out_idx))

    def _check(self,context):
        self._check_print(os.path.exists(self.out_idx),self.out_idx)

    def clean_file(self,filename):
        cmdtpl = "if test -e $DST ; then rm -f  $DST ; fi ; "
        cmd    = Template(cmdtpl).substitute(DST=filename)
        shexec.execmd(cmd)

    def _clean(self,context):
        self.clean_file(self.out_idx)

