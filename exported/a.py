import dataviewer


@dataviewer.export_text(dataviewer.number)
def a(a):
    assert isinstance(a, int)
    return a * 3


@dataviewer.export_tabular(dataviewer.number, d=dataviewer.number)
def b(a, b, c=None, d=3):
    return [
        [1, 2, 3],
        [4, 5, 6]
    ]
