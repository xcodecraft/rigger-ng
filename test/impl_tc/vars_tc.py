#coding=utf8
import logging
import interface,res

from   impl.rg_model  import *
from   base.tc_tools   import *

_logger = logging.getLogger()


class vars_tc(rigger_tc):
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

        testbox   = res.module()
        v1       = res.vars()
        v1.X     = "a"
        v1.Y     = "b"

        e1       = res.echo()
        e1.value = "${X}/${Y}"

        testbox.append(v1)
        testbox.append(e1)

        context = interface.run_context()
        run     = res_runner(testbox)
        run.config(context)

