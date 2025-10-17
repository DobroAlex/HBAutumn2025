"""
It's easily possible to break the second test by accidentally writing to `Colors` class.

Furthermore, test_2 now has an unobvious error while test_1 silently passed
"""


class Colors:
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"


def test_1():
    ...
    Colors.RED = "White"
    ...


def test_2():
    ...
    assert Colors.RED == "Red"
