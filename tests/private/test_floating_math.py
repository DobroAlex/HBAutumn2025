"""
Floating-point math can introduce unexpected quirks
since a CPU doesn't represent floating numbers like you do with a pen on a paper.
"""

from decimal import Decimal
from fractions import Fraction

import pytest


@pytest.mark.parametrize(
    "km_distance",
    (1, 10, 100, 1_000, 10_000, 100_000, 1_000_000)
)
def test_bad_travel(km_distance):
    """Always fails due to accumulated inaccuracy."""
    total_traveled: float = 0.
    # Each step being 1m
    step_size: float = 0.001
    steps_count: int = int(km_distance / step_size)

    expected_total_traveled = steps_count * step_size

    for step in range(steps_count):
        total_traveled += step_size

    print(f"Expected to travel: {expected_total_traveled}")
    print(f"Actually traveled: {total_traveled}")
    assert total_traveled == expected_total_traveled


@pytest.mark.parametrize(
    "km_distance",
    (1, 10, 100, 1_000, 10_000, 100_000, 1_000_000)
)
def test_better_travel_with_centimeters(km_distance):
    """
    In this example we use integer only centimeters computations.

    This is much better as it doesn't suffer from the floating-point induced loss
    of precision.

    However, it's not always possible to use integer-only math.
    """
    total_traveled: float = 0.
    step_size: int = 1
    steps_count: int = int(km_distance / step_size)

    expected_total_traveled = steps_count * step_size

    for step in range(steps_count):
        total_traveled += step_size

    print(F"Expected to travel: {expected_total_traveled}")
    print(f"Actually traveled: {total_traveled}")
    assert total_traveled == expected_total_traveled


@pytest.mark.parametrize(
    "km_distance",
    (1, 10, 100, 1_000, 10_000, 100_000, 1_000_000)
)
def test_better_travel_with_decimal(km_distance):
    """
    The same as the original
    but precision is increased by using Decimal to avoid float-related inaccuracy.
    """

    total_traveled: Decimal = Decimal(value="0")
    step_size: Decimal = Decimal("0.001")
    steps_count = int(km_distance / step_size)

    expected_total_traveled = steps_count * step_size

    for step in range(steps_count):
        total_traveled += step_size

    print(F"Expected to travel: {expected_total_traveled}")
    print(f"Actually traveled: {total_traveled}")
    assert total_traveled == expected_total_traveled


def test_bad_collision():
    """Always fails as actual result goes below zero"""
    distance: float = 10_000.

    while distance > 0:
        distance -= 0.01

    assert distance == 0


def test_better_collision():
    """Now let's use Fractions"""
    distance: int | Fraction = 10_000
    step = Fraction(numerator=1, denominator=1000)  # 1/1000
    while distance > 0:
        # mypy will complain a lot due to type mismatch (int -> Fraction)
        # but it doesn't matter as distance is converted to Fraction after the
        # first step.
        distance -= step

    assert distance == 0
    assert int(distance) == 0
    assert float(distance) == 0
