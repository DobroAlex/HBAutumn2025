"""
It's always a good idea to use time zone aware dates.
It's even better to use UTC dates as they don't suffer from DST & other wall clock adjustments.
"""

from datetime import datetime

import pytz


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
    """This one doesn't have the same flaw as dates are UTC converted."""
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

    assert (dt2 - dt1).seconds == (dt2 - dt1).seconds == 60 * 60
    assert (dt1 - dt2).days == -(dt2 - dt1).days == -1


###############################


def test_datetime_comparison_flaky_without_utc():
    """
    This test compares two globally equal dates,
     but they're treated as unequal dates due to timezone differences.
    """
    dt_utc = datetime(
        2025, 9, 18, 10, 0, 0, tzinfo=pytz.utc
    )
    london_tz = pytz.timezone("Europe/London")
    dt_london = london_tz.localize(
        datetime(2025, 9, 18, 11, 0, 0)
    )
    assert dt_utc == dt_london


def test_datetime_comparison_fixed_with_utc():
    """This test converts both dates to UTC so TZ doesn't mess up the comparison."""
    dt_utc = datetime(
        2025, 9, 18, 10, 0, 0, tzinfo=pytz.utc
    )
    london_tz = pytz.timezone("Europe/London")
    dt_london = london_tz.localize(
        datetime(2025, 9, 18, 11, 0, 0)
    )
    # Convert both datetimes to UTC for a consistent comparison
    dt_utc_converted = dt_utc.astimezone(pytz.utc)
    dt_london_converted = dt_london.astimezone(pytz.utc)

    assert dt_utc_converted == dt_london_converted
