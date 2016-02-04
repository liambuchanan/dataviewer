"""
Some basic examples of html form type specification etc.
"""

import dataviewer as dv


@dv.export(dv.number)
def mul3(a):
    """multipies a by 3"""
    assert isinstance(a, int)
    return dv.Text(a * 3)


@dv.export(dv.number, dv.number, c=dv.number, d=dv.number)
def nonsense_table(a, b, c=None, d=3):
    """builds a table containing supplied values"""
    return dv.Table(
        [
            [a, b, c if c is not None else 0],
            [d, 5, 6]
        ]
    )
