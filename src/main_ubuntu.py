from main_impl import *
if __name__ == '__main__':
    set_modul_path()
    import interface,impl
    import ubuntu
    import pylon
    impl.setup()
    ubuntu.setup()
    pylon.setup()
    main()

