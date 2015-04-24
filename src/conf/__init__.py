#coding=utf-8
import interface
import logging
from utls.rg_io import rg_logger

if len(interface.registed_conf.items() ) == 0 :
    raise interface.rigger_exception("@res.__init__ no regist res to module" )

for res,module in interface.registed_conf.items() :
    code = "from %s import %s" %(module,res )
    rg_logger.debug( " load module: %s" %code  )
    try :
        exec code
    except  Exception as e :
        raise interface.rigger_exception("@res.__init__ code error: %s \n %s" %(code,e) )


