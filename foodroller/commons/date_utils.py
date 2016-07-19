import calendar
import datetime


class Date(object):
    # Get the weekday as string from a given date
    @staticmethod
    def weekday_from_date(date):
        return calendar.day_name[date.weekday()]

    # Get the end date of a time period
    @staticmethod
    def get_end_date(start_date, num_days):
        return start_date + datetime.timedelta(days=num_days-1)

    # Create a dictionary containing a time period in the format: {'Tuesday': 23.02.1987, 'Wednesday': 24.02.1987,... }
    @staticmethod
    def create_days_dict(start_date, num_days):
        days_in_row = [{start_date: Date.weekday_from_date(start_date)}]
        for x in range(1, num_days):
            next_day = start_date + datetime.timedelta(days=x)
            days_in_row.append({next_day: Date.weekday_from_date(next_day)})

        return days_in_row
