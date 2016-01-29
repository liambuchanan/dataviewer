"""
This is a filler docstring. It says nothing useful
"""

import dataviewer as dv


@dv.export(dv.number)
def div100(a):
    """divides a by 100"""
    return dv.Text(a/100)


@dv.export(dv.text, dv.number)
def n_by_b_of_x(x, n):
    """create an n by n table of x"""
    rows = []
    for i in xrange(n):
        rows.append(n*[x])
    return dv.Table(rows)
