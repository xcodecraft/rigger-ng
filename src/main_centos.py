from main_impl import *
if __name__ == '__main__':
    set_modul_path()
    import interface,impl
    import centos
    import pylon
    impl.setup()
    centos.setup()
    pylon.setup()
    main()

