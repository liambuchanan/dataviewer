import abc
import json

import plotly.utils


__all__ = ["Text", "Table", "PlotlyObject"]


class Builder(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, result):
        self.result = result

    @abc.abstractmethod
    def to_html(self):
        return
"""
    def to_json(self):
        # TODO builders should optionally implement to_json
        pass

    def to_csv(self):
        # TODO builders should optionally implement to_csv
        pass
"""


class Text(Builder):
    def to_html(self):
        return "<pre>{}</pre>".format(self.result)


class Table(Builder):
    def to_html(self):
        return "<table>{}</table>".format(
            "".join(
                "<tr>{}</tr>".format(html_row)
                for html_row in (
                    "".join("<td>{}</td>".format(cell) for cell in row)
                    for row in self.result
                )
            )
        )


class PlotlyObject(Builder):
    def to_html(self):
        return (
            """
            <script src="/static/plotly.min.js"></script>
            <div id="content"></div>
            <script>
                content_div = document.getElementById('content');
                Plotly.plot(content_div, [{}]);
            </script>
            """.format(
                json.dumps(self.result, cls=plotly.utils.PlotlyJSONEncoder)
            )
        )
