import collections
import glob
import imp
import inspect
import os

import dataviewer


class Arg(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.value = None
        self.html_input_type = type.name

    @property
    def html_input_value(self):
        return "" if self.value is None else str(self.value)

    def update_value(self, value):
        self.value = value

    def __repr__(self):
        return "Arg({}, {})".format(self.name, self.value)


class Kwarg(Arg):
    def __init__(self, name, type, default):
        super(Kwarg, self).__init__(name, type)
        self.value = default

    def __repr__(self):
        return "Kwarg({}, {})".format(self.name, self.value)


class ExportedModule(collections.Mapping):
    def __init__(self, module, exported_functions):
        self.name = module.__name__
        self.doc = module.__doc__
        self.exported_functions = collections.OrderedDict(
            (fn_name, ExportedFunction(fn))
            for fn_name, fn in exported_functions
        )

    def __getitem__(self, key):
        return self.exported_functions[key]

    def __len__(self):
        return len(self.exported_functions)

    def __iter__(self):
        return iter(self.exported_functions)

    def __repr__(self):
        return "ExportedModule.{}({})".format(
            self.name,
            ", ".join(self.exported_functions)
        )


class ExportedFunction(object):
    def __init__(self, fn):
        args, _, _, defaults = inspect.getargspec(fn)
        defaults = defaults if defaults is not None else []
        arg_types = fn.arg_types
        kwarg_types = fn.kwarg_types
        num_args = len(args) if defaults is None else len(args) - len(defaults)

        self.fn = fn
        self.name = fn.__name__
        self.doc = fn.__doc__
        self.args = [Arg(name, type) for name, type in zip(args, arg_types)]
        for arg in args[len(self.args):num_args]:
            self.args.append(Arg(arg, kwarg_types.get(arg, dataviewer.text)))
        self.kwargs = [
            Kwarg(arg, kwarg_types.get(arg, dataviewer.text), default)
            for (arg, default) in zip(args[num_args:], defaults)
        ]

    def update_values(self, query_params):
        for arg in self.args + self.kwargs:
            value = query_params.get(arg.name)
            if (
                value is not None and
                not (isinstance(value, basestring) and len(value) == 0)
            ):
                arg.update_value(arg.type.parse(value))

    def execute(self):
        args = [arg.value for arg in self.args]
        kwargs = {kwarg.name: kwarg.value for kwarg in self.kwargs}
        return self.fn(*args, **kwargs)

    def html_result(self):
        return self.fn.result_to_html(self.execute())

    def __repr__(self):
        return "ExportedFunction.{}({})".format(
            self.name,
            ", ".join(map(repr, self.args + self.kwargs))
        )


def find_exported(modules_dir):
    def _is_exported_fn(fn):
        return (
            inspect.isfunction(fn) and
            inspect.getmodule(fn) is module and
            getattr(fn, "exported", False)
        )
    exported_modules = []
    for module_path in sorted(glob.glob(modules_dir + "/*.py")):
        try:
            module_name = os.path.split(module_path)[-1][:-3]
            module = imp.load_source(module_name, module_path)
            exported_functions = inspect.getmembers(module, _is_exported_fn)
            if len(exported_functions) > 0:
                exported_modules.append(
                    (
                        module_name,
                        ExportedModule(module, exported_functions)
                    )
                )
        except Exception as e:
            # TODO log exception properly
            print e
            import traceback
            traceback.print_exc()
    return collections.OrderedDict(exported_modules)
