"""
Get a time tuple in a timezone a specified number of hours away from UTC.

This program runs under MicroPython on the ESP-32.
"""
import time

timezone_hours = -7

# Just use localtime() if you want time in UTC
# def get_utc():
#     return time.localtime()

# Parameter tz: offset from UTC in hours. Defaults to US MST -7


def get_local_time(tz=timezone_hours):
    """
    Uses time.time(), which returns seconds since epoch (not MacroPython's
    epoch!) and converts it to a real local time tz hours away from
    UTC.  Because MicroPython doesn't know about timezones, time.localtime()
    only returns the local time for people in the vicinity of Greenwich,
    England--in the winter--i.e., UTC.

    This routine does not know about DST.

    :param tz: Number of hours +/- from UTC to the desired time, i.e., -7 for
        USA Mountain standard time.
    :return: A time tuple:
        (year, month, mday, hour, min, sec, wday, yday)
        Note:  I haven't investigated which weekday is 0.  I suspect Sunday.
    """
    seconds_since_epoch = time.time()

    timezone_offset = tz * 3600

    corrected_since_epoch = seconds_since_epoch + timezone_offset
    ct = time.localtime(corrected_since_epoch)
    return ct

# A reminder of the order of the tuple:
#human_time = f"Yr: {ct[0]} Mo: {ct[1]} MDy: {ct[2]} Hr: {ct[3]} Mn: {ct[4]} Sc: {ct[5]} WDy: {ct[6]} YDy: {ct[7]}"
# (Year,
#  Month,
#  Month day,
#  Hour,
#  Minute,
#  Second,
#  Week day,
#  Year day)
