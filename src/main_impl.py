#!/usr/bin/pylon.27
import sys ,  os ,logging,getopt ,setting
import interface

def set_modul_path() :
    root  = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(root)
    sys.path.append(os.path.join(root,"extends/res") )

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


def main():
    import impl.rg_run , impl.rg_args
    from   utls.rg_io import rgio
    parser = impl.rg_args.rarg_parser()
    parser.parse(sys.argv[1:] )
    setting_debug(parser.argv)

    opts,args = getopt.getopt(sys.argv[1:],"d:s:e:c:")
    # rars_file = os.getcwd() + "/_rg/.rigger-ng-v1.data"
    if setting.debug :
        rargs  = impl.rg_args.run_args.load()
        rargs.parse_update(parser)
        impl.rg_run.run_rigger(rargs,parser.argv)
    else:
        try :
            #import pdb
            #pdb.set_trace() ;
            rargs  = impl.rg_args.run_args.load()
            rargs.parse_update(parser)
            impl.rg_run.run_rigger(rargs,parser.argv)

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


# if __name__ == '__main__':
#     set_modul_path()
#     import interface,impl
#     import ubuntu
#     impl.setup()
#     ubuntu.setup()
#     main()
#
