import calendar

__author__ = 'stefan'

def weekday_from_date(date):
    return calendar.day_name[date.weekday()]

