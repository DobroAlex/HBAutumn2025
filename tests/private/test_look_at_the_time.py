from datetime import datetime

import pytz


# Let's talk about time.time() vs time.perf_counter()
# One is real-world time, another is performance benchmarking tool / intervals measurer.

# time.time() might suck at measuring time < 1 second or < 500 ms
# due to possible rounding errors.

# time.perf_counter() is non adjustable, monotonic, more precise.

# time.time() is good for real-world time(stamps) & system time.
# time.perf_counter() is good for measuring short intervals.

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

    assert (dt2 - dt1).seconds == (dt2 - dt1).seconds == 60 * 60
    assert (dt1 - dt2).days == -1

# an example of an NTP synchronization causing issues with
# monotonic time should be here, but coding it is wild
