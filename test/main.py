import  re , os , string ,  getopt ,sys , unittest,logging


def load_module():
    code= """
from res.mysql import  mysql
"""
    return code
if __name__ == '__main__':

    root  = os.path.dirname(os.path.realpath(__file__))
    root  = os.path.dirname(root)
    sys.path.append(os.path.join(root,"src") )

    logging.basicConfig(level=logging.INFO,filename='test.log')
    # _logger.addHandler(logging.StreamHandler(sys.stderr))
    import interface
    from   utls.rg_io import rgio
    interface.load_res("from res.mysql import mysql")

    from impl_tc.yaml_tc  import *
    from impl_tc.tpl_tc   import *
    from impl_tc.vars_tc  import *
    from impl_tc.args_tc  import *
    from impl_tc.cmd_tc   import *
    from res_tc.mysql_tc  import *



    unittest.main()
    # try :
    # except error.user_break as e:
    #     rgio.error(e)
    # except error.badargs_exception  as e :
    #     print("\nerror:")
    # rgio.error(e)
    # runargs.help()
    #
    # except getopt.GetoptError as e:
    #     print("\nerror:")
    # print(e)
    # runargs.help()
    # except error.depend_exception as e :
    #     e.monitor.out()
    # except interface.rigger_exception as e:
    #     pass
         # rgio.error(e)
