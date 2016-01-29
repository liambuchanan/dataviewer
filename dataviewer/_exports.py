import abc


__all__ = ["export_text", "export_tabular"]


class export(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *arg_types, **kwarg_types):
        self.arg_types = arg_types
        self.kwarg_types = kwarg_types

    def __call__(self, fn):
        fn.arg_types = self.arg_types
        fn.kwarg_types = self.kwarg_types
        fn.exported = True
        fn.result_to_html = self.result_to_html
        return fn

    @abc.abstractmethod
    def result_to_html(self, result):
        return


class export_text(export):
    def result_to_html(self, result):
        return "<pre>{}</pre>".format(result)


class export_tabular(export):
    def result_to_html(self, result):
        return "<table>{}</table>".format(
            "".join(
                "<tr>{}</tr>".format(html_row)
                for html_row in (
                    "".join("<td>{}</td>".format(cell) for cell in row)
                    for row in result
                )
            )
        )
