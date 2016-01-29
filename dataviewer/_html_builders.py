import abc


__all__ = ["Text", "Table"]


class HtmlBuilder(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, result):
        self.result = result

    @abc.abstractmethod
    def to_html(self):
        return


class Text(HtmlBuilder):
    def to_html(self):
        return "<pre>{}</pre>".format(self.result)


class Table(HtmlBuilder):
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
