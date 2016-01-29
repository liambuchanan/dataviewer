import glob
import os
import imp
import inspect
from collections import OrderedDict

from flask import abort, Flask, render_template, request

import dataviewer


app = Flask(__name__)

MODULE_DIR = "../exported"


def find_exported_modules():
    def _is_exported_fn(fn):
        return (
            inspect.isfunction(fn) and
            inspect.getmodule(fn) is module and
            getattr(fn, "exported", False)
        )
    exported_modules = []
    for module_path in sorted(glob.glob(MODULE_DIR + "/*.py")):
        try:
            module_name = os.path.split(module_path)[-1][:-3]
            module = imp.load_source(module_name, module_path)
            exported_functions = inspect.getmembers(module, _is_exported_fn)
            if len(exported_functions) > 0:
                exported_modules.append(
                    (module_name, OrderedDict(exported_functions))
                )
        except Exception as e:
            # log exception
            print e
            pass
    return OrderedDict(exported_modules)


EXPORTED = find_exported_modules()


@app.route("/")
def index():
    return render_template(
        "index.html",
        module_names=EXPORTED.keys()
    )


@app.route("/<module_name>")
def module(module_name):
    if module_name in EXPORTED:
        return render_template(
            "module.html",
            module_name=module_name,
            functions=EXPORTED[module_name]
        )
    else:
        abort(404)


class Arg(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.html_type = type.name


class Kwarg(Arg):
    def __init__(self, name, type, default):
        super(Kwarg, self).__init__(name, type)
        self.default = default
        self.html_default = ""


class ExportedFunction(object):
    def __init__(self, module_name, function_name):
        fn = EXPORTED[module_name][function_name]
        args, _, _, defaults = inspect.getargspec(fn)
        defaults = defaults if defaults is not None else []
        arg_types = fn.arg_types
        kwarg_types = fn.kwarg_types
        num_args = len(args) if defaults is None else len(args) - len(defaults)

        self.fn = fn
        self.args = [Arg(name, type) for name, type in zip(args, arg_types)]
        for arg in args[len(self.args):num_args]:
            self.args.append(Arg(arg, kwarg_types.get(arg, dataviewer.text)))
        self.kwargs = [
            Kwarg(arg, kwarg_types.get(arg, dataviewer.text), default)
            for (arg, default) in zip(args[num_args:], defaults)
        ]

    def __call__(self, query_params):
        args = []
        for arg in self.args:
            args.append(
                query_params.get(arg.name, type=arg.type.parse)
            )

        def _get_kwarg_value(kwarg, query_param):
            if query_param is None or len(query_param) == 0:
                return kwarg.default
            else:
                return kwarg.type.parse(query_param)

        kwargs = {
            kwarg.name: _get_kwarg_value(kwarg, query_params.get(kwarg.name))
            for kwarg in self.kwargs
        }

        return self.fn(*args, **kwargs)


@app.route("/<module_name>/<function_name>")
def function(module_name, function_name):
    try:
        if module_name in EXPORTED and function_name in EXPORTED[module_name]:
            ef = ExportedFunction(module_name, function_name)
            try:
                content = ef(request.args)
            except Exception as e:
                content = str(e)
            return render_template(
                "function.html",
                args=ef.args,
                kwargs=ef.kwargs,
                content=content
            )
        else:
            abort(404)
    except Exception as e:
        print e

if __name__ == "__main__":
    app.run()
