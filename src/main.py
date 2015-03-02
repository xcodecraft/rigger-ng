#!/usr/bin/pylon.27
import sys ,  os ,logging

root  = os.path.dirname(os.path.realpath(__file__))
root  = os.path.dirname(root)
sys.path.append(os.path.join(root,"src") )

if __name__ == '__main__':
    import interface,impl
    impl.setup()
    from utls.rg_io import rgio

    # logging.basicConfig(level=logging.INFO,filename='run.log')
    logging.basicConfig(level=logging.DEBUG,filename='run.log')
    try :

        import impl.rg_run , impl.rg_args
        rargs  = impl.rg_args.run_args()
        parser = impl.rg_args.rarg_parser()
        parser.parse(rargs,sys.argv[1:] )
        rargs.prj.conf = "_rg/prj.yaml"
        # rargs.rg.conf  = "_rg/os.yaml"
        impl.rg_run.run_rigger(rargs,parser.argv)

    except interface.user_break as e:
        rgio.error(e)
    except interface.badargs_exception  as e :
        print("\nerror:")
        rgio.error(e)
        runargs.help()
    # except getopt.GetoptError as e:
    #     print("\nerror:")
    #     print(e)
    #     runargs.help()
    except interface.depend_exception as e :
        e.monitor.out()
    except interface.rigger_exception as e:
         rgio.error(e)
