"""Module with other small functions"""
from __future__ import print_function
from __future__ import unicode_literals
#  Standard library imports

# Third party imports

# Local imports


def timedelta_nice_format(td_object):
    """Create string with nice formatted time duration"""
    if td_object is None:
        return "None"
    seconds = int(td_object.total_seconds())
    if seconds == 0:
        return "0 seconds"
    periods = [
        ('year', 60*60*24*365),
        ('month', 60*60*24*30),
        ('day', 60*60*24),
        ('hour', 60*60),
        ('minute', 60),
        ('second', 1)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)
