#coding=utf-8
import logging
import interface
import utls.rg_io

from utls.rg_io import rg_logger

def setup() :
    # interface.regist_res("pylon_router,pylon_autoload,php_class_parser"                , "pylon.pylon_res")
    interface.regist_res("pylon_router,pylon_autoload"                , "pylon.pylon_res")

