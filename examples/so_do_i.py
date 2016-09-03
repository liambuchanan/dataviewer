"""
This is a filler docstring. It says nothing useful
"""
import random

import dataviewer as dv

import plotly.graph_objs as go


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


@dv.export(dv.number)
def get_plot(num_points):
    random_x = range(num_points)
    random_y = [random.random() for _ in random_x]
    return dv.PlotlyObject(go.Scatter(
        x=random_x,
        y=random_y
    ))
