#coding=utf-8
import logging
import interface
import utls.rg_io

from utls.rg_io import rg_logger


def setup() :
    interface.regist_res("fpm,fpm_pool,nginx_conf,mysql", "centos.port")
    interface.regist_res("daemon,daemon_php",             "centos.port")

