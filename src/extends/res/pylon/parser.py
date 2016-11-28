
#coding=utf-8
import logging
import interface
import os ,re
import utls.tpl
import sys

from utls.rg_io  import rg_logger
from utls.rg_sh  import shexec
from string import *
from res.base   import *

_logger = logging.getLogger()


class php_rest_parser:
    def __init__(self) :
        self.rest_rule = None
        self.rest_svcs = {}


    def out2file(self,dstfile,version):
        for k,v in self.rest_svcs.items():
            match = re.match('^.*\$.*$',k, re.IGNORECASE)
            if match :
                if version == 1 :
                    dstfile.write( "/zzzzzz%s : %s\n" %(k,v))
                if version == 2 :
                    dstfile.write( "%s : %s\n" %(k,v))
            else :
                dstfile.write( "%s : %s\n" %(k,v))

    def parse_file(self,srcfile,dstfile,version=1) :
        with  open(srcfile,'r') as sf:
            for line in sf.readlines():
                self.parse(line)
            self.out2file(dstfile,version)

    def parse(self, line) :

        if self.rest_rule :
            #////
            if re.match('^/{2}.*$',line, re.IGNORECASE) :
                return
            #空行
            if re.match('^\s*$',line, re.IGNORECASE) :
                return
            match = re.match('^\s*class\s+(\w+).*implements\s+XService.*$',line, re.IGNORECASE)
            if match  :
                cls_name = match.group(1)
                for one in self.rest_rule.split(",") :
                    self.rest_svcs[one] = cls_name
            self.rest_rule = None

        match = re.match('^\s*class\s+(\w+).*implements\s+XService\s+\/\/@REST_RULE:\s+(.+)$',line, re.IGNORECASE)
        if match :
            cls_name  = match.group(1)
            rest_rule = match.group(2)
            for one in rest_rule.split(",") :
                self.rest_svcs[one] = cls_name

        match = re.match('^\s*\/\/@REST_RULE:\s+(.+)',line, re.IGNORECASE)
        if match :
            self.rest_rule = match.group(1)

class php_class_parser:
    """
    """
    def __init__(self):
        """docstring for __init__"""
        self.namespace = ""
        self.clsnames  = []
    def out2file(self,filepath,clspath,clsname) :
        for item  in self.clsnames :
            clspath.write(Template("$CLS,$PATH\n").substitute(PATH=filepath,CLS=item))
            clsname.write(Template("cls_$LOWCLS,$CLS\n").substitute(CLS=item,LOWCLS=item.lower()))

    def parse_file(self,srcfile,replace,clspath,clsname) :

        with  open(srcfile,'r') as sf:
            for line in sf.readlines():
                self.parse(line)
        if len(replace) > 0 :
           srcfile= srcfile.replace(replace,'')
        self.out2file(srcfile,clspath,clsname)


    def parse(self, line) :
        match = re.match('^\s*namespace\s+([\w\\\]+)\s*;',line, re.IGNORECASE)
        if match :
            self.namespace = match.group(1)

        clsname = None
        match = re.match('^\s*class\s+(\w+).*$',line, re.IGNORECASE)
        if match :
            clsname = match.group(1)

        match = re.match('^\s*trait\s+(\w+).*$',line, re.IGNORECASE)
        if match :
            clsname = match.group(1)

        match = re.match('^\s*abstract\s*class\s+(\w+)\s*{?',line, re.IGNORECASE)
        if match :
            clsname = match.group(1)

        match = re.match('^\s*interface\s+(\w+).*$',line,flags=re.IGNORECASE)
        if match :
            clsname = match.group(1)
        if clsname != None :
            if len(self.namespace) == 0 :
                self.clsnames.append(clsname)
            else :
                self.clsnames.append(self.namespace +  "\\" + clsname)
