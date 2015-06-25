#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
from impl.rg_args import *


_logger = logging.getLogger()



class args_tc(base.tc_tools.rigger_tc):
    def test_parse(self) :
        rargs  = run_args()
        parser = rarg_parser()
        cmd    = "conf -e dev -s test"
        parser.parse(cmd.split(' '))
        rargs.parse_update(parser)
        self.assertEqual(str(rargs),cmd )


        rargs  = run_args()
        cmd    = "start -e dev -s api"
        parser.parse(cmd.split(' '))
        rargs.parse_update(parser)
        self.assertEqual(str(rargs),cmd )

    def test_save(self):
        from utls.rg_var import value_of
        save_file = value_of("${HOME}/devspace/rigger-ng/test/data/rigger.data")

        rargs          = run_args()
        rargs.rg.save_path = save_file
        rargs.prj.env  = "diy"
        rargs.prj.sys  = "api,test"
        rargs.prj.cmds = "conf,start"
        rargs.save()

        loaded  = run_args.load(save_file)
        self.assertEqual(loaded.prj.env  , rargs.prj.env)
        self.assertEqual(loaded.prj.sys  , rargs.prj.sys)
        self.assertEqual(loaded.prj.cmds , [])


