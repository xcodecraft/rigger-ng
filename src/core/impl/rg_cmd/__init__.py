import interface
import logging

from utls.rg_io import  rg_logger

if len(interface.registed_cmd.items() ) == 0 :
    raise interface.rigger_exception("@cmd.__init__ no regist cmd to module" )

for cmd,module in interface.registed_cmd.items() :
    code = "from %s import %s_cmd" %(module,cmd )
    rg_logger.debug( " load module: %s" %code  )
    try :
        exec code
    except  Exception as e :
        raise interface.rigger_exception("@cmd.__init__ code error: %s \n %s" %(code,e) )

