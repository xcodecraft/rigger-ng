# from impl.rg_prj import system , project, module
# from inner import vars , echo , assert_eq

import interface
import logging

_logger = logging.getLogger()

if len(interface.registed_resource.items() ) == 0 :
    raise interface.rigger_exception("@res.__init__ no regist res to module" )

for res,module in interface.registed_resource.items() :
    code = "from %s import %s" %(module,res )
    _logger.debug( " load module: %s" %code  )
    try :
        exec code

    except  Exception as e :
        raise interface.rigger_exception("@res.__init__ code error: %s \n %s" %(code,e) )


