#coding=utf-8
import logging
import interface
import utls.rg_io

from utls.rg_io import rg_logger


def setup() :
    interface.regist_res("require_file,require_url_content,require_url_code", "check.check_impl")
