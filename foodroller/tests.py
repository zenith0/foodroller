from django.test import TestCase
from foodroller.models import Category, Food


class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Suppe")
        Food.objects.create(name="FreeDatenSuppe", category="Suppe")

    def test_get_food(self):
        category = Category.objects.get(name="Suppe")
        food = category.get_food()
        self.assertEqual(food.name, "FreeDatenSuppe")

