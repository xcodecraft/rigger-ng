import  re , os , string ,  getopt ,sys , unittest,logging


def setup_env() :
    root  = os.path.dirname(os.path.realpath(__file__))
    root  = os.path.dirname(root)
    sys.path.append(os.path.join(root,"src") )
    import core.run_env
    core.run_env.set_modul_path()

    os.environ['PRJ_ROOT'] = os.environ['HOME'] + "/devspace/rigger-ng"
    logging.basicConfig(level=logging.DEBUG,filename='test.log')


if __name__ == '__main__':

    setup_env()

    import interface,impl
    impl.setup()


    from impl_tc.vars_tc  import *
    from utls_tc.json_tc   import *
    from impl_tc.yaml_tc  import *
    from utls_tc.tpl_tc   import *
    from utls_tc.rg_var_tc import *
    from impl_tc.args_tc  import *
    from impl_tc.cmd_tc   import *
    from res_tc.files_tc  import *
    from res_tc.inner_tc  import *
    from res_tc.shell_tc  import *

    unittest.main()
