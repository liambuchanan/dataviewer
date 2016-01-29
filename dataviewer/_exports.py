class export(object):
    def __init__(self, *arg_types, **kwarg_types):
        self.arg_types = arg_types
        self.kwarg_types = kwarg_types

    def __call__(self, fn):
        fn.arg_types = self.arg_types
        fn.kwarg_types = self.kwarg_types
        fn.exported = True
        return fn
