"""
This is a module docstring
"""

import dataviewer


@dataviewer.export_text(dataviewer.number)
def div100(a):
    """divides a by 100"""
    return a/100


@dataviewer.export_tabular(dataviewer.number, dataviewer.number)
def n_by_b_of_x(x, n):
    """create an n by n table of x"""
    rows = []
    for i in xrange(n):
        rows.append(n*[x])
    return rows
