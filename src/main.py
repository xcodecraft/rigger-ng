#!/usr/bin/pylon.27
import sys ,  os ,logging,getopt ,setting

root  = os.path.dirname(os.path.realpath(__file__))
root  = os.path.dirname(root)
sys.path.append(os.path.join(root,"src") )

def setting_debug(opts) :
    log_level = logging.ERROR
    for opt,val in opts.items() :
        if opt == '-d' :
            setting.debug       = True
            setting.debug_level = int(val)
            if int(val) == 1 :
                log_level = logging.INFO
            if int(val) >= 2 :
                log_level = logging.DEBUG
    logging.basicConfig(level=log_level,filename='run.log')
    if setting.debug :
        console   = logging.StreamHandler()
        console.setLevel(log_level)
        # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # console.setFormatter(formatter)
        logging.getLogger().addHandler(console)



if __name__ == '__main__':
    import interface,impl
    import impl.rg_run , impl.rg_args
    from   utls.rg_io import rgio
    impl.setup()
    parser = impl.rg_args.rarg_parser()
    parser.parse(sys.argv[1:] )
    setting_debug(parser.argv)

    opts,args = getopt.getopt(sys.argv[1:],"d:s:e:")
    rars_file = os.getcwd() + "/_rg/.rigger-ng-v1.data"
    if setting.debug :
        rargs  = impl.rg_args.run_args.load(rars_file)
        rargs.parse_update(parser)
        impl.rg_run.run_rigger(rargs,parser.argv)
        rargs.save(rars_file)
    else:
        try :

            rargs  = impl.rg_args.run_args.load(rars_file)
            rargs.parse_update(parser)
            impl.rg_run.run_rigger(rargs,parser.argv)
            rargs.save(rars_file)

        except interface.user_break as e:
            rgio.error(e)
        except interface.badargs_exception  as e :
            print("\nerror:")
            rgio.error(e)
            runargs.help()
        except getopt.GetoptError as e:
            print("\nerror:")
            print(e)
            runargs.help()
        except interface.depend_exception as e :
            e.monitor.out()
        except interface.rigger_exception as e:
             rgio.error(e)
