from django.test import TestCase
from foodroller.models import Category, Food, Ingredient
from foodroller.utils import weekday_from_date, filter_food_by_duration, get_end_date, create_days_dict, \
    category_food_dict
import datetime

__author__ = 'stefan'


class UtilsTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Kategorie").save()
        Category.objects.create(name="Kategorie2").save()
        category = Category.objects.get(name="Kategorie")
        category2 = Category.objects.get(name="Kategorie2")

        food_29 = Food.objects.create(name="30 min", slug="30min", duration=datetime.timedelta(minutes=29))
        food_29.categories.add(category)
        food_29.save()
        food_59 = Food.objects.create(name="1 hr", slug="1hr", duration=datetime.timedelta(minutes=59))
        food_59.categories.add(category)
        food_59.save()
        food_119 = Food.objects.create(name="2 hr", slug="2hr", duration=datetime.timedelta(minutes=119))
        food_119.categories.add(category)
        food_119.save()
        food_121 = Food.objects.create(name="2 hr+", slug="2hr+", duration=datetime.timedelta(minutes=121))
        food_121.categories.add(category)
        food_121.save()

        food = Food.objects.create(name="Test", slug="test")
        food.categories.add(category2)
        food.save()

    def test_get_weekday(self):
        my_date = datetime.datetime(2016, 2, 14)
        week_day = weekday_from_date(my_date)
        self.assertEqual(week_day, "Sunday")

    def test_filter_food_by_duration(self):
        food_29 = Food.objects.get(name="30 min")
        food_59 = Food.objects.get(name="1 hr")
        food_119 = Food.objects.get(name="2 hr")
        food_121 = Food.objects.get(name="2 hr+")

        food_list = Food.objects.all()

        res_list = filter_food_by_duration(food_list, "1")
        self.assertTrue(food_29 in res_list)
        self.assertFalse(food_59 in res_list)
        self.assertFalse(food_119 in res_list)
        self.assertFalse(food_121 in res_list)

        res_list = filter_food_by_duration(food_list, "2")
        self.assertTrue(food_29 in res_list)
        self.assertTrue(food_59 in res_list)
        self.assertFalse(food_119 in res_list)
        self.assertFalse(food_121 in res_list)

        res_list = filter_food_by_duration(food_list, "3")
        self.assertTrue(food_29 in res_list)
        self.assertTrue(food_59 in res_list)
        self.assertTrue(food_119 in res_list)
        self.assertFalse(food_121 in res_list)

        res_list = filter_food_by_duration(food_list, "4")
        self.assertFalse(food_29 in res_list)
        self.assertFalse(food_59 in res_list)
        self.assertFalse(food_119 in res_list)
        self.assertTrue(food_121 in res_list)

        res_list = filter_food_by_duration(food_list, None)
        self.assertTrue(food_29 in res_list)
        self.assertTrue(food_59 in res_list)
        self.assertTrue(food_119 in res_list)
        self.assertTrue(food_121 in res_list)

    def test_get_end_date(self):
        now = datetime.datetime.now()
        days = 6
        end_data = get_end_date(now, days)
        self.assertEqual(end_data, now + datetime.timedelta(days=days-1))

    def test_create_days_dict(self):
        now = datetime.datetime.now()
        list = create_days_dict(now, 4)
        for k, v in list[0].items():
            self.assertEqual(k, now)
        for k, v in list[1].items():
            self.assertEqual(k, now + datetime.timedelta(days=1))
        for k, v in list[2].items():
            self.assertEqual(k, now + datetime.timedelta(days=2))
        for k, v in list[3].items():
            self.assertEqual(k, now + datetime.timedelta(days=3))

    def test_category_food_dict(self):
        dict = category_food_dict()
        cat1 = Category.objects.get(name="Kategorie")
        cat2 = Category.objects.get(name="Kategorie2")
        food_29 = Food.objects.get(name="30 min")
        food_59 = Food.objects.get(name="1 hr")
        food_119 = Food.objects.get(name="2 hr")
        food_121 = Food.objects.get(name="2 hr+")
        food_test = Food.objects.get(name="Test")
        for k, v in dict.items():
            if k == cat1:
                self.assertTrue(food_29 in v)
                self.assertTrue(food_59 in v)
                self.assertTrue(food_119 in v)
                self.assertTrue(food_121 in v)
                self.assertFalse(food_test in v)
            elif k == cat2:
                self.assertFalse(food_29 in v)
                self.assertFalse(food_59 in v)
                self.assertFalse(food_119 in v)
                self.assertFalse(food_121 in v)
                self.assertTrue(food_test in v)
