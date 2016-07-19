from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory
from foodroller.models import Category, Food, Ingredient
from foodroller.utils import filter_food_by_duration, \
    category_food_dict, get_cached_food_plan, get_already_rolled, update_food_plan, update_current_plan, \
    update_already_rolled, get_food_from_cached_plan, new_already_rolled, filter_food_by_category_name
import datetime

__author__ = 'stefan'


class SessionUtilsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.food_plan = [{'day': '01.01.16', 'food': 'Pizza'},
                     {'day': '02.01.16', 'food': 'Pizza'}]
        self.already_rolled = ['Pizza', 'Pasta']
        self.request = RequestFactory().get("/")
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()
        self.request.session['plan'] = self.food_plan
        self.request.session['already_rolled'] = self.already_rolled

    def test_get_cached_food_plan(self):
        test_plan = get_cached_food_plan(self.request)
        self.assertEqual(self.food_plan, test_plan)

    def test_get_already_rolled(self):
        test_already_rolled = get_already_rolled(self.request)
        self.assertEqual(self.already_rolled, test_already_rolled)

    def test_update_food_plan(self):
        self.setUp()
        new_food_plan = [{'day': '03.01.16', 'food': 'Pasta'},
                         {'day': '04.01.16', 'food': 'Pie'}]
        update_food_plan(self.request, new_food_plan)
        test_plan = get_cached_food_plan(self.request)
        self.assertEqual(test_plan, new_food_plan)

    def test_update_current_plan_override(self):
        self.setUp()
        new_plan = [{'day': '01.01.16', 'food': 'Pizza'},
                     {'day': '02.01.16', 'food': 'Pasta'}]
        update_current_plan(self.request, 'Pasta', '02.01.16')
        test_plan = get_cached_food_plan(self.request)
        self.assertEqual(new_plan, test_plan)

    def test_update_already_rolled(self):
        self.setUp()
        already_rolled = ['Ham', 'Eggs', 'Soup']
        update_already_rolled(self.request, already_rolled)
        test_already_rolled = get_already_rolled(self.request)
        self.assertEqual(already_rolled, test_already_rolled)

    def test_get_food_from_cached_plan(self):
        self.setUp()
        food_list = ['Pizza']
        test_list = get_food_from_cached_plan(self.request)
        self.assertEqual(food_list, test_list)
        new_food_plan = [{'day': '03.01.16', 'food': 'Pasta'},
                         {'day': '04.01.16', 'food': 'Pie'}]
        update_food_plan(self.request, new_food_plan)
        test_list = get_food_from_cached_plan(self.request)
        self.assertTrue('Pasta' in test_list and 'Pie' in test_list)

    def test_new_already_rolled(self):
        self.setUp()
        already_rolled = new_already_rolled(self.request)
        self.assertEqual(already_rolled, ['Pizza'])
        already_rolled = ['Pizza', 'Pasta', 'Cheese', 'Pie', 'Ham']
        update_already_rolled(self.request, already_rolled)
        already_rolled = new_already_rolled(self.request)
        self.assertEqual(already_rolled, ['Pizza'])
        new_food_plan = [{'day': '03.01.16', 'food': 'Pasta'},
                         {'day': '04.01.16', 'food': 'Pie'}]
        update_food_plan(self.request, new_food_plan)
        already_rolled = new_already_rolled(self.request)
        self.assertTrue('Pasta' in already_rolled and 'Pie' in already_rolled)




class FoodUtilsTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Kategorie").save()
        Category.objects.create(name="Kategorie2").save()
        category = Category.objects.get(name="Kategorie")
        category2 = Category.objects.get(name="Kategorie2")

        food_29 = Food.objects.create(name="30 min", duration=datetime.timedelta(minutes=29))
        food_29.categories.add(category)
        food_29.save()
        food_59 = Food.objects.create(name="1 hr", duration=datetime.timedelta(minutes=59))
        food_59.categories.add(category)
        food_59.save()
        food_119 = Food.objects.create(name="2 hr", duration=datetime.timedelta(minutes=119))
        food_119.categories.add(category)
        food_119.save()
        food_121 = Food.objects.create(name="3 hr", duration=datetime.timedelta(minutes=121))
        food_121.categories.add(category)
        food_121.save()

        food = Food.objects.create(name="Test", slug="test")
        food.categories.add(category2)
        food.save()

    def test_filter_food_by_duration(self):
        food_29 = Food.objects.get(name="30 min")
        food_59 = Food.objects.get(name="1 hr")
        food_119 = Food.objects.get(name="2 hr")
        food_121 = Food.objects.get(name="3 hr")

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

    def test_category_food_dict(self):
        dict = category_food_dict()
        cat1 = Category.objects.get(name="Kategorie")
        cat2 = Category.objects.get(name="Kategorie2")
        food_29 = Food.objects.get(name="30 min")
        food_59 = Food.objects.get(name="1 hr")
        food_119 = Food.objects.get(name="2 hr")
        food_121 = Food.objects.get(name="3 hr")
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

    def test_filter_food_by_category_name(self):
        category = Category.objects.get(name="Kategorie2")
        food_list = filter_food_by_category_name(category.name)
        food = Food.objects.get(name="Test")
        self.assertEqual(len(food_list), 1)
        self.assertTrue(food in food_list)







