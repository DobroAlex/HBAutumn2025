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
    step_size: float = 0.01
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
    """In this example we use integer only centimeters computations."""
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
    step_size: Decimal = Decimal("0.1")
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
    distance = 10_000
    step = Fraction(numerator=1, denominator=100)  # 1/100
    while distance > 0:
        distance -= step  # mypy will complain a lot

    assert distance == 0
    assert int(distance) == 0
    assert float(distance) == 0


def test_bad_fraction():
    assert (1 / 3 * 3000000000000000000000000000000) == 1000000000000000000000000000000


def test_better_fraction():
    assert (Fraction(numerator=1, denominator=3) * 3000000000000000000000000000000) == 1000000000000000000000000000000
