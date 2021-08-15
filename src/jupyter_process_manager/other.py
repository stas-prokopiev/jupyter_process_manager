"""Module with other small functions"""
from __future__ import print_function
#  Standard library imports
from math import floor
from math import log10

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


def rtnsd(float_num, int_digits=1):
    """[summary]
    Args:
        float_num (float): float number to round
        int_digits (int): How many significant digits you need. Defaults to 1.
    """
    if not isinstance(float_num, (float, int)):
        raise TypeError("Unable to round number with type %s " % (
            str(type(float_num))
        ))


    if not float_num:
        return 0.0
    int_sign_digits = floor(log10(abs(float_num)))
    return round(float_num, int_digits - int(int_sign_digits) - 1)
