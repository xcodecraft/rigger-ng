class singleton(object):
    def __new__(cls, *args,** kwargs):
        if '_inst' not in vars(cls):
            cls._inst = super(singleton,cls).__new__(cls, * args, **kwargs)
        return  cls._inst
