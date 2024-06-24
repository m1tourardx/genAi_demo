from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser
from copy import copy

def convert_to_datetime(time_string, time_param: str = 'start'):
    if 'now' in time_string:
        date = datetime.now()
        return date

    number, unit = time_string.split(
        '-')[0][:-1], time_string.split('-')[0][-1]
    number = int(number)

    units = {'w': 'weeks', 'd': 'days', 'M': 'months', 'y': 'years',
            'h': 'hours', 'm': 'months', 's': 'seconds'}

    now = datetime.utcnow()
    if unit in units:
        date = now - relativedelta(**{units[unit]: number})
    else:
        try:
            date = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            date = datetime.strptime(time_string, '%Y-%m-%d')
    
    if time_param == 'end':
        date = date.replace(hour=23, minute=59, second=59)
    
    return date
