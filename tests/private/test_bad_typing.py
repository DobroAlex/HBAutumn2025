"""
Some examples of bad usage of dynamic typing
&
how it can be caught using linters & type checkers.
"""

from typing import TypeVar, runtime_checkable, Protocol

import pytest


def do_addition(a, b):
    return a + b


def test_surprising_type():
    assert do_addition(1, 2) == 3
    assert do_addition(1.2, 3.4) == 4.6
    assert do_addition("10", "12") == "1012"
    assert do_addition([1, ], [2, ]) == [1, 2, ]
    assert do_addition((1,), [2, ])


@runtime_checkable
class SupportAddition(Protocol):
    def __add__(self: 'T', other: 'T') -> 'T':
        ...


T = TypeVar('T', bound=SupportAddition)


def __do_addition_new(a: T, b: T) -> T:
    return a + b


def test_better_type_check() -> None:
    assert __do_addition_new(5, 10) == 15
    assert __do_addition_new("5", "10") == "510"
    with pytest.raises(TypeError):
        assert __do_addition_new(5, "10") == "510"  # Is not caught by mypy but caught by IDE

    __do_addition_new(7, {'a': 1})  # Caught by mypy in --strict mode


