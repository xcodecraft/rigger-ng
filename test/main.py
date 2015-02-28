import  re , os , string ,  getopt ,sys , unittest,logging

if __name__ == '__main__':

    root  = os.path.dirname(os.path.realpath(__file__))
    root  = os.path.dirname(root)
    sys.path.append(os.path.join(root,"src") )

    logging.basicConfig(level=logging.INFO,filename='test.log')
    # _logger = logging.getLogger()
    # _logger.addHandler(logging.StreamHandler(sys.stderr))

    from impl_tc.yaml_tc  import *
    from impl_tc.tpl_tc   import *
    from impl_tc.vars_tc  import *
    from impl_tc.args_tc  import *
    from impl_tc.cmd_tc   import *
    unittest.main()
