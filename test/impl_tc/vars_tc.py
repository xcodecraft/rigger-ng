#coding=utf8
import logging
import interface,res

# from   impl.rg_model  import *
from   base.tc_tools   import *

_logger = logging.getLogger()


class vars_tc(rigger_tc):
    def test_vars(self):
        jfile = os.path.dirname(os.path.dirname(__file__)) + "/data/data.json"
        v1       = res.vars()
        v1.X     = "a"
        v1.Y     = "b"
        v1._json = "%s:%s" %(jfile,"/env/dev/")
        context = interface.run_context()
        v1._before(context)


    def test_vars_echo(self):
        """
        test this
        ------------------------
        !R.vars:
            X : "a"
            Y : "b"
        !R.echo:
            value : "${X}/${Y}"
        """

        testbox  = res.modul()
        v1       = res.vars()
        v1.X     = "a"
        v1.Y     = "b"

        e1       = res.echo()
        e1.value = "${X}/${Y}"

        testbox.append(v1)
        testbox.append(e1)

        context = interface.run_context()
        interface.control_call( testbox,interface.controlable._config,context,'_config')

