import os
import datetime
from cryptography.fernet import Fernet

def get_key_from_file():
    if os.path.exists('fernet.key'):
        with open('fernet.key', 'rb') as fkey:
            return fkey.read()
    else:
        with open('fernet.key', 'wb') as fkey:
            new_fkey = Fernet.generate_key()
            fkey.write(new_fkey)
            return new_fkey


def get_total_duty(last_login:datetime.datetime, last_logout:datetime.datetime)->tuple:
    """Returns `hours`,`minutes`,`seconds`"""
    total_duty = last_logout - last_login
    hours,remainder = divmod(total_duty.total_seconds(),3600)
    minutes,seconds = divmod(remainder,60)
    return int(hours),int(minutes),int(seconds)

def get_overtime_duty(last_login:datetime.datetime, last_logout:datetime.datetime)->tuple:
    """Returns `hours`,`minutes`,`seconds`"""
    total_duty = last_logout - last_login
    overtime_duty = max(total_duty - datetime.timedelta(hours=8), datetime.timedelta())
    hours,remainder = divmod(overtime_duty.total_seconds(),3600)
    minutes,seconds = divmod(remainder,60)
    return int(hours),int(minutes),int(seconds)

def get_night_shift(start_datetime:datetime.datetime, end_datetime:datetime.datetime)->tuple:
    """Returns `hours`,`minutes`,`seconds`"""
    total_seconds = 3600 * len(get_night_duty_range_hours(start_datetime,end_datetime))
    hours,remainder = divmod(total_seconds,3600)
    minutes,seconds = divmod(remainder,60)
    return int(hours),int(minutes),int(seconds)

def get_night_duty_range_hours(start_datetime:datetime.datetime, end_datetime:datetime.datetime) ->list:
    hours = []
    while start_datetime <= end_datetime:
        hour = start_datetime.hour
        if hour < 6 or hour > 22:
            hours.append(hour)
        start_datetime += datetime.timedelta(hours=1)
    return hours

