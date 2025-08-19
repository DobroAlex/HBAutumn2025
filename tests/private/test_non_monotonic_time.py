"""
Examples of time.time() being unreliable due to its implementation & nature.

time.time() is  a wall clack & thus it may suffer from a time zone change
or NTP SYNC adjustment.

time.monotonic() is much safer for benchmarking here.

THIS EXAMPLE IS FOR WINDOWS ONLY!
THIS EXAMPLE REQUIRES ADMIN PRIVILEGES TO RUN!
"""
import datetime
import time

from dateutil import tz as dateutil_tz
import pytz


def ntp_sync(seconds_ago: int = 10) -> None:
    """Simulate an NTP sync that brings system time `seconds_age` seconds before."""
    import win32api
    target_date = (datetime.datetime.now(tz=dateutil_tz.tzlocal())
                   - datetime.timedelta(seconds=seconds_ago))

    target_date_utc = target_date.astimezone(pytz.UTC)
    day_of_the_week = target_date_utc.isocalendar()[2]

    # This one requires UTC time
    win32api.SetSystemTime(
        target_date_utc.year,
        target_date_utc.month,
        day_of_the_week,
        target_date_utc.day,
        target_date_utc.hour,
        target_date_utc.minute,
        target_date_utc.second,
        0,
    )


def slow_process(run_for: float) -> None:
    """Imitate running a long job by calling time.sleep()"""
    return time.sleep(run_for)


def test_time_measurement_no_ntp():
    """A perfect case scenario. No NTP sync so test always passes"""
    start = time.time()
    slow_process(run_for=3)
    stop = time.time()
    delta = stop - start
    assert 0 <= delta <= 5


def test_time_measurement_ntp_appears():
    """Oh no, ntp sync will cause this one to fail with time being -2."""
    start = time.time()
    slow_process(run_for=3)
    ntp_sync(seconds_ago=5)
    stop = time.time()
    delta = stop - start
    assert 0 <= delta <= 5


def first_stupid_solution():
    """
    We can try fixing the case by extending ranges.
    But it makes the test gibberish.
    """
    start = time.time()
    slow_process(run_for=3)
    ntp_sync(seconds_ago=5)
    stop = time.time()
    delta = stop - start
    assert 0 - 3 <= delta <= 5 + 5


def test_good_solution_with_monotonic_time():
    """
    Replace time.time (a wall clock)
    with time.monotonic (a stopwatch) and rest easily.
    """
    start = time.monotonic()
    ntp_sync(seconds_ago=60)
    slow_process(run_for=3)
    stop = time.monotonic()
    delta = stop - start
    assert 0 <= delta <= 5
