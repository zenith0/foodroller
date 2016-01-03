__author__ = 'stefan'
from django.test import TestCase
from foodroller.models import Category, Food


class CategoryTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Soup")
        category_2 = Category.objects.create(name="Salad")
        food = Food.objects.create(name="FreeDatenSuppe")
        food.categories.add(category)
        food.save()
        food_2 = Food.objects.create(name="FreeSalad")
        food_2.categories.add(category_2, category)
        food_2.save()

    def test_get_food(self):
        category = Category.objects.get(name="Soup")
        food = category.get_food()
        self.assertEqual(food[0].name, "FreeDatenSuppe")
        self.assertEqual(food[1].name, "FreeSalad")
        category_2 = Category.objects.get(name="Salad")
        food = category_2.get_food()
        self.assertEqual(food[0].name, "FreeSalad")

