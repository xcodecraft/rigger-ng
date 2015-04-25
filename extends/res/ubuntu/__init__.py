#coding=utf-8
import logging
import interface
import utls.rg_io

from utls.rg_io import rg_logger


def setup() :
    interface.regist_res("fpm,fpm_pool"   , "ubuntu.fpm")
    interface.regist_res("mysql"      , "ubuntu.mysql")
    interface.regist_res("nginx_conf" , "ubuntu.websvc")
    interface.regist_res("varnishd"   , "ubuntu.varnishd")

