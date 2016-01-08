__author__ = 'stefan'
from django.test import TestCase
from foodroller.models import Category, Food, Ingredient


class CategoryTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Soup")
        category_2 = Category.objects.create(name="Salad")
        food = Food.objects.create(name="FreeDatenSuppe", slug="freedatensuppe")
        food.categories.add(category)
        food.save()
        food_2 = Food.objects.create(name="FreeSalad", slug="freesalad")
        food_2.categories.add(category_2, category)
        food_2.save()
        in1 = Ingredient.objects.create(name="Salat", amount="1")
        in2 = Ingredient.objects.create(name="Zucker", amount="1EL")
        in1.food = food_2
        in2.food = food_2
        in1.save()
        in2.save()

    def test_get_food(self):
        category = Category.objects.get(name="Soup")
        food = category.get_food()
        self.assertEqual(food[0].name, "FreeDatenSuppe")
        self.assertEqual(food[1].name, "FreeSalad")
        category_2 = Category.objects.get(name="Salad")
        food = category_2.get_food()
        self.assertEqual(food[0].name, "FreeSalad")

    def test_get_ingredients(self):
        food = Food.objects.get(name="FreeSalad")
        in_list = food.get_ingredients()
        self.assertEqual(in_list[0].name, "Salat")
        self.assertEqual(in_list[0].amount, "1")
        self.assertEqual(in_list[1].name, "Zucker")
        self.assertEqual(in_list[1].amount, "1EL")

