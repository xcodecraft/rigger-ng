import  re , os , string ,  getopt ,sys , unittest,logging


if __name__ == '__main__':

    root  = os.path.dirname(os.path.realpath(__file__))
    root  = os.path.dirname(root)
    sys.path.append(os.path.join(root,"src") )

    logging.basicConfig(level=logging.DEBUG,filename='test.log')
    import interface,impl
    impl.setup()

    from impl_tc.yaml_tc  import *
    from utls_tc.tpl_tc   import *
    from utls_tc.rg_var_tc import *
    from impl_tc.vars_tc  import *
    from impl_tc.args_tc  import *
    from impl_tc.cmd_tc   import *
    from res_tc.mysql_tc  import *
    from res_tc.files_tc  import *
    from res_tc.inner_tc  import *
    # from res_tc.varnishd_tc  import *
    from res_tc.fpm_tc  import *
    unittest.main()
