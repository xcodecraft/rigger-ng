#coding=utf-8
import logging
import interface


from utls.rg_io  import rgio,rg_logger
from utls.rg_sh  import shexec
from res.base import *
from string import *
import utls.rg_var , utls.check

class mysql_base(interface.resource,res_utls):

    def _allow(self,context) :
        return True
    def _before(self,context):
        with res_context(self.__class__.__name__) :
            self.host     = utls.rg_var.value_of(self.host)
            self.name     = utls.rg_var.value_of(self.name)
            self.password = utls.rg_var.value_of(self.password)
            self.user     = utls.rg_var.value_of(self.user)
            self.sql      = utls.rg_var.value_of(self.sql)

    def _start(self,context):
        self._data(context)

    def _data(self,context):
        mysql  = self.bin
        cmdtpl = '$MYSQL -h$HOST $DBNAME -u$USER -p$PASSWD < $SQL'
        shexec.execmd(Template(cmdtpl).substitute(MYSQL=mysql,HOST=self.host ,DBNAME=self.name,USER=self.user,PASSWD=self.password,SQL=self.sql),True)

    def _info(self,context,level):
        if  level  <= 0  :
            return 
        rgio.struct_out("mysql: %s" %(self.name))
