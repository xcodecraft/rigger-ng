#coding=utf-8
import logging
import interface
_logger = logging.getLogger()

from impl.rg_var import  value_of
from impl.rg_sh  import  shexec
from string import *

class mysql(interface.resource):
    """
    !R.mysql:
        host: "127.0.0.1"
        init: "init.sql"
    """
    host    = "localhost"
    name    = ""
    user    = ""
    password = ""
    init    = ""
    root    = "root"
    rootpwd = ""
    allow_addr = "%"

    def _allow(self,context) :
        return True
    def _before(self,context):
        self.host       = value_of(self.host)
        self.name       = value_of(self.name)
        self.password   = value_of(self.password)
        self.user       = value_of(self.user)
        self.init       = value_of(self.init)
        self.root       = value_of(self.root)
        self.rootpwd    = value_of(self.rootpwd)
        self.allow_addr = value_of(self.allow_addr)

    def _data(self,context):
        sql = "DROP DATABASE IF EXISTS $DBNAME;CREATE DATABASE $DBNAME DEFAULT CHARACTER SET UTF8;"
#        sql +="GRANT ALL PRIVILEGES ON $DBNAME.* TO '$USER'@'$ADDR' IDENTIFIED BY '$PASSWD' ;"
        cmd   = Template(sql).substitute(DBNAME=self.name,USER=self.user,PASSWD=self.password,ADDR=self.allow_addr)
        # mysql = get_env_conf().mysql
        mysql = "/usr/bin/mysql"
        if len(self.rootpwd) > 0 :
            shexec.execmd("%s -h%s -u%s -p%s -e \"%s\" " %(mysql ,self.host,self.root, self.rootpwd,cmd) )
        else:
            print("create database , please input mysql root password: ")
            shexec.execmd("%s -h%s -u%s -p  -e \"%s\" " %(mysql ,self.host,self.root,cmd) )
        cmdtpl  = '$MYSQL -h$HOST $DBNAME -u$USER -p$PASSWD < $SQL'
        shexec.execmd(Template(cmdtpl).substitute(MYSQL=mysql,HOST=self.host ,DBNAME=self.name,USER=self.user,PASSWD=self.password,SQL=self.init),True)
