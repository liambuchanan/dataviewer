from flask import abort, Flask, render_template, request

from exported import find_exported


app = Flask(__name__)
MODULE_DIR = "../exported"
EXPORTED = find_exported(MODULE_DIR)


@app.route("/")
def index():
    return render_template(
        "index.html",
        modules=EXPORTED.values(),
    )


@app.route("/<module_name>")
def module(module_name):
    if module_name in EXPORTED:
        return render_template(
            "module.html",
            module=EXPORTED[module_name],
            functions=EXPORTED[module_name].values()
        )
    else:
        abort(404)


@app.route("/<module_name>/<function_name>")
def function(module_name, function_name):
    if (
        module_name in EXPORTED and
        function_name in EXPORTED[module_name]
    ):
        module = EXPORTED[module_name]
        function = module[function_name]
        result = ""
        if len(request.args) > 0:
            try:
                function.update_values(request.args)
                result = function.html_result()
            except Exception as e:
                result = "<pre>{}</pre>".format(e)
        return render_template(
            "function.html",
            module=module,
            function=function,
            result=result
        )
    else:
        abort(404)


if __name__ == "__main__":
    app.run()
