"""
Now test_1 will be highlighted by mypy with the `--strict` flag
plus it will fail at runtime with a clear error without breaking test_2.
"""
import enum


class Colors(enum.Enum):
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
