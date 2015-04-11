#coding=utf-8
import logging
import interface

class php_def(interface.resource):
    bin  = "/usr/bin/php"
    fpm  = "/usr/sbin/php-fpm"
    def _before(self,context):
        context.php_def = self

class mysql_def(interface.resource) :
    bin = "/usr/bin/mysql"
    def _before(self,context):
        context.mysql_def = self
    pass

class nginx_def(interface.resource) :
    pass

class apache_def(interface.resource) :
    pass
