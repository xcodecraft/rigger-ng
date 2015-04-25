#coding=utf-8
import logging
import interface

class php_def(interface.resource):
    bin           = "/usr/bin/php"
    fpm           = "/usr/sbin/php-fpm"
    fpm_conf_root = "/etc/php5/fpm/pool.d/"
    def _before(self,context):
        context.php_def = self

class mysql_def(interface.resource) :
    bin = "/usr/bin/mysql"
    def _before(self,context):
        context.mysql_def = self
    pass

class nginx_def(interface.resource) :
    bin       = "/usr/sbin/service nginx"
    conf_root = "/etc/nginx/sites-enabled/"
    def _before(self,context):
        context.nginx_def = self
    pass

class apache_def(interface.resource) :
    pass


