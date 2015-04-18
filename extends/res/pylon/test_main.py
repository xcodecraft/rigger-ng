import  re , os , string ,  getopt ,sys , unittest,logging

def setup_env() :
    root  = os.path.dirname(os.path.realpath(__file__))
    root  = os.path.dirname(root)
    root  = os.path.dirname(root)
    root  = os.path.dirname(root)
    sys.path.append(os.path.join(root,"src") )
    sys.path.append(os.path.join(root,"test") )
    sys.path.append(os.path.join(root,"extends/res") )
    os.environ['PRJ_ROOT'] = os.environ['HOME'] + "/devspace/rigger-ng"
    logging.basicConfig(level=logging.DEBUG,filename='test.log')

if __name__ == '__main__':

    setup_env()

    import interface,impl
    impl.setup()
    import pylon
    pylon.setup()

    from pylon_tc   import *
    unittest.main()
