import datetime
from django.test import TestCase
from foodroller.commons.date_utils import Date


class DateUtilsTestCase(TestCase):
    def test_get_weekday(self):
        my_date = datetime.datetime(2016, 2, 14)
        week_day = Date.weekday_from_date(my_date)
        self.assertEqual(week_day, "Sunday")

    def test_get_end_date(self):
        now = datetime.datetime.now()
        days = 6
        end_data = Date.get_end_date(now, days)
        self.assertEqual(end_data, now + datetime.timedelta(days=days-1))

    def test_create_days_dict(self):
        now = datetime.datetime.now()
        list = Date.create_days_dict(now, 4)
        for k, v in list[0].items():
            self.assertEqual(k, now)
        for k, v in list[1].items():
            self.assertEqual(k, now + datetime.timedelta(days=1))
        for k, v in list[2].items():
            self.assertEqual(k, now + datetime.timedelta(days=2))
        for k, v in list[3].items():
            self.assertEqual(k, now + datetime.timedelta(days=3))