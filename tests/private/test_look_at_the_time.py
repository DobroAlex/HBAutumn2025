from datetime import datetime
import time

import pytest
import pytz


def __fast_calculation_function() -> int:
    # It's something generally fast
    return sum(i for i in range(100))


def test_bad_performance_measure():
    """This test lacks precision
    as time.time() is better suited for working with seconds-sized time."""
    start = time.time()
    __fast_calculation_function()
    stop = time.time()
    print(f"Elapsed with time.time(): {(stop - start):.9f}")

    start = time.perf_counter()
    __fast_calculation_function()
    stop = time.perf_counter()
    # This has better precision
    print(f"Elapsed with time.perf_counter(): {stop - start}")


def test_good_time_span():
    """time.time() is better with seconds-sized time spans."""
    start = time.time()
    time.sleep(10)
    stop = time.time()
    print(f"Elapsed with time.time: {stop - start}")

    start = time.perf_counter_ns()
    time.sleep(10)
    stop = time.perf_counter_ns()
    print(f"Elapsed with time.perf_counter_ns: {(stop - start) / 10 ** 9}")


@pytest.mark.xfail
def test_bad_jumping_dst():
    """This test has weired 0 seconds diff due to a dst change."""

    # Time zone with DST (New York)
    NY_tz = pytz.timezone('America/New_York')

    # First occurrence of 1:30 AM (before DST ends)
    dt1 = NY_tz.localize(datetime(2023, 11, 5, 1, 30), is_dst=True)

    # Second occurrence of 1:30 AM (after DST ends)
    dt2 = NY_tz.localize(datetime(2023, 11, 5, 1, 30), is_dst=False)

    # One hour passed, OK!
    assert (dt2 - dt1).seconds == 60 * 60

    # Zero diff :'c
    assert (dt1 - dt2).seconds == 60 * 60


def test_better_jumping_dst():
    # Time zone with DST (New York)
    NY_tz = pytz.timezone('America/New_York')

    # First occurrence of 1:30 AM (before DST ends)
    dt1 = NY_tz.localize(datetime(2023, 11, 5, 1, 30), is_dst=True)

    # Second occurrence of 1:30 AM (after DST ends)
    dt2 = NY_tz.localize(datetime(2023, 11, 5, 1, 30), is_dst=False)

    UTC_tz = pytz.timezone('UTC')

    # Convert both to a steady DST-less format
    dt1 = dt1.astimezone(tz=UTC_tz)
    dt2 = dt2.astimezone(tz=UTC_tz)

    assert (dt2 - dt1).seconds == 60 * 60
    assert (dt1 - dt2).days == -1

# an example of an NTP synchronization causing issues with
# monotonic time should be here, but coding it is wild
