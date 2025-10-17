"""
An alternative approach is to use a frozen dict.
test_1 will fail at runtime with a clear error without breaking test_2.
"""
import frozendict

COLORS = frozendict.frozendict({"RED": "Red", "GREEN": "Green", "BLUE": "Blue"})


def test_1():
    ...
    COLORS["RED"] = "White"
    ...


def test_2():
    ...
    assert COLORS["RED"] == "Red"
