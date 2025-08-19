from decimal import Decimal

import pytest


@pytest.mark.xfail
def test_bad_travel():
    """Always fails due to accumulated inaccuracy."""
    # Make a million of steps each being 0.01m -> 1 cm.
    # Expected result is 1 million cm == 10_000 m.
    total_traveled: float = 0.
    steps_count: int = 1_000_000
    step_size: float = 0.01

    expected_total_traveled = steps_count * step_size

    for step in range(steps_count):
        total_traveled += step_size

    print(F"Expected to travel: {expected_total_traveled}")
    print(f"Actually traveled: {total_traveled}")
    assert total_traveled == expected_total_traveled


def test_better_travel_with_centimeters():
    """In this example we use integer only centimeters computations."""
    total_traveled: float = 0.
    steps_count: int = 1_000_000
    step_size: int = 1

    expected_total_traveled = steps_count * step_size

    for step in range(steps_count):
        total_traveled += step_size

    print(F"Expected to travel: {expected_total_traveled}")
    print(f"Actually traveled: {total_traveled}")
    assert total_traveled == expected_total_traveled


def test_better_travel_with_decimal():
    """
    The same as the original
    but precision is increased by using Decimal to avoid float-related inaccuracy.
    """

    total_traveled: Decimal = Decimal(value=0.)
    steps_count: int = 1_000_000
    step_size: Decimal = Decimal("0.1")

    expected_total_traveled = steps_count * step_size

    for step in range(steps_count):
        total_traveled += step_size

    print(F"Expected to travel: {expected_total_traveled}")
    print(f"Actually traveled: {total_traveled}")
    assert total_traveled == expected_total_traveled


@pytest.mark.xfail
def test_bad_collision():
    """Always fails as actual result goes below zero"""
    distance = 10_000

    while distance > 0:
        distance -= 0.01

    assert distance == 0
