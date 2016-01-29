from flask import abort, Flask, render_template, request

from exported_function import find_exported_functions


app = Flask(__name__)
MODULE_DIR = "../exported"
EXPORTED_FUNCTIONS = find_exported_functions(MODULE_DIR)


@app.route("/")
def index():
    return render_template(
        "index.html",
        module_names=EXPORTED_FUNCTIONS.keys()
    )


@app.route("/<module_name>")
def module(module_name):
    if module_name in EXPORTED_FUNCTIONS:
        return render_template(
            "module.html",
            module_name=module_name,
            functions=EXPORTED_FUNCTIONS[module_name].keys()
        )
    else:
        abort(404)


@app.route("/<module_name>/<function_name>")
def function(module_name, function_name):
    try:
        if (
            module_name in EXPORTED_FUNCTIONS and
            function_name in EXPORTED_FUNCTIONS[module_name]
        ):
            e_fn = EXPORTED_FUNCTIONS[module_name][function_name]
            result = ""
            if len(request.args) > 0:
                try:
                    e_fn.update_values(request.args)
                    result = e_fn.html_result()
                except Exception as e:
                    result = "<pre>{}</pre>".format(e)
            return render_template(
                "function.html",
                args=e_fn.args,
                kwargs=e_fn.kwargs,
                result=result
            )
        else:
            abort(404)
    except:
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    app.run()
