"""Utility functions

Collection of utility functions.
"""

import time

def get_days(dtime=None):
    """Get date as days since epoch

    Gets the specified time as number of days since epoch. Time
    is specified as number of secs since epoch and the default
    is to use the current time.

    return -- number of days since epoch
    dtime  -- no. of secs since epoch
    """
    if dtime is None:
        dtime = time.time()

    return int(dtime/86400)


def remspace(value):
    """Remove all spaces from string

    Remove all whitespace in a string (not just whitespace at
    the start/end).

    For example "A B  C" -> "ABC"

    return -- whitespace stripped string
    value  -- input string
    """
    return "".join(value.split())

