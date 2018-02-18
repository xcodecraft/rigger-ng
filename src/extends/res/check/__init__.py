#coding=utf-8
import logging
import interface
import utls.rg_io

from utls.rg_io import rg_logger


def setup() :
    interface.regist_res("assert_file_sha,assert_url_sha"      , "check.check_impl")
