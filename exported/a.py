import dataviewer


@dataviewer.export(dataviewer.number)
def a(a):
    assert isinstance(a, int)
    return a * 3


@dataviewer.export(dataviewer.number, d=dataviewer.number)
def b(a, b, c=None, d=3):
    return None
