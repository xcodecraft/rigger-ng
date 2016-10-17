#coding=utf-8
import logging
import interface
import utls.rg_io

from utls.rg_io import rg_logger


def setup() :
    interface.regist_res("fpm,nginx_conf,mysql"      , "websys.port")
    interface.regist_res("daemon,daemon_php,crontab" , "websys.port")
    interface.regist_res("hosts"                     , "websys.port")
    interface.regist_res("beanstalkd,varnishd"       , "websys.port")
