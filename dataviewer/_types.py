from datetime import datetime

__all__ = ["text", "number", "checkbox", "date"]

# add Noneable types?
# add options type?


class Text(object):
    def __init__(self):
        self.name = "text"
        self.parse = str
text = Text()


class Number(object):
    def __init__(self):
        self.name = "number"
        self.parse = int
number = Number()


class Checkbox(object):
    def __init__(self):
        self.name = "checkbox"
        self.parse = bool
checkbox = Checkbox()


class Date(object):
    def __init__(self):
        self.name = "date"
        self.parse = lambda inp: datetime.strptime(inp, "%Y-%m-%d").date()
date = Date()
