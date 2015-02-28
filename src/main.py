#!/usr/bin/pylon.27
import sys ,  os

root  = os.path.dirname(os.path.realpath(__file__))
root  = os.path.dirname(root)
sys.path.append(os.path.join(root,"src") )

if __name__ == '__main__':
    import interface
    import impl.rg_run , impl.rg_args
    rargs  = impl.rg_args.run_args()
    parser = impl.rg_args.rarg_parser()
    parser.parse(rargs,sys.argv[1:] )
    rargs.prj.conf = "_rg/prj.yaml"
    # rargs.rg.conf  = "_rg/os.yaml"
    impl.rg_run.run_rigger(rargs,parser.argv)

