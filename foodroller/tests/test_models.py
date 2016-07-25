import sys
import datetime

__author__ = 'stefanperndl'

from django.test import TestCase
from foodroller.models import Category, Food, Ingredient, Foodplan, Day


def create_ing_for_food(name, amount, food):
    ingredient = Ingredient(name=name, amount=amount)
    ingredient.food = food
    ingredient.save()


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

    def test_category_str(self):
        category = Category.objects.get(name="Soup")
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), "Soup")

    def test_category_verbose(self):
        category = Category.objects.get(name="Soup")
        self.assertEqual(category._meta.verbose_name, 'Category')
        self.assertEqual(category._meta.verbose_name_plural, 'Categories')

    def test_get_food(self):
        category = Category.objects.get(name="Soup")
        food = category.get_food()
        self.assertEqual(food[0].name, "FreeDatenSuppe")
        self.assertEqual(food[1].name, "FreeSalad")
        category_2 = Category.objects.get(name="Salad")
        food = category_2.get_food()
        self.assertEqual(food[0].name, "FreeSalad")


class FoodTestCase(TestCase):

    def setUp(self):
        food = Food.objects.create(name="Food1", slug="food1")
        food.save()
        in1 = Ingredient.objects.create(name="Salat", amount="1")
        in2 = Ingredient.objects.create(name="Zucker", amount="1EL")
        in1.food = food
        in2.food = food
        in1.save()
        in2.save()

    def test_food_str(self):
        food = Food.objects.get(name='Food1')
        self.assertEqual(food.__str__(), 'Food1')

    def test_get_ingredients(self):
        food = Food.objects.get(name="Food1")
        in_list = food.get_ingredients()
        self.assertEqual(in_list[0].name, "Salat")
        self.assertEqual(in_list[0].amount, "1")
        self.assertEqual(in_list[1].name, "Zucker")
        self.assertEqual(in_list[1].amount, "1EL")

    def test_last_cooked(self):
        food = Food.objects.get(name="Food1")
        today_str = datetime.datetime.now().strftime('%d-%m-%y')
        food.set_last_cooked(today_str, '%d-%m-%y')
        self.assertEqual(food.get_last_cooked(), today_str)

    def test_merge_ingredients(self):
        food = Food.objects.create(name="Food2")
        food.save()
        create_ing_for_food("Zucker", "1g", food)
        create_ing_for_food("Zucker", "2g", food)
        create_ing_for_food("Zucker", "3 g", food)
        create_ing_for_food("Wasser", "1 ml", food)
        food = Food.objects.get(name="Food2")
        ingredients = food.merge_ingredients()
        self.assertEqual(len(ingredients), 2)


class IngredientsTestCase(TestCase):
    def setUp(self):
        ingredient = Ingredient.objects.create(name='Ingredient', amount='1.1g')
        ingredient.save()

    def test_get_amount(self):
        ingredient = Ingredient.objects.get(name='Ingredient')
        self.assertEqual(ingredient.get_amount(), '1.1')

    def test_get_unit(self):
        ingredient = Ingredient.objects.get(name='Ingredient')
        self.assertEqual(ingredient.get_unit(), 'g')

    def test_normalization(self):
        ingredient = Ingredient.objects.create(name='test1', amount='1,1g')
        ingredient.save()
        ingredient = Ingredient.objects.get(name='test1')
        self.assertEqual(ingredient.get_amount(), '1.1')
        self.assertEqual(ingredient.get_unit(), 'g')

        ingredient = Ingredient.objects.create(name='test2', amount='1,1 g')
        ingredient.save()
        ingredient = Ingredient.objects.get(name='test2')
        self.assertEqual(ingredient.get_amount(), '1.1')
        self.assertEqual(ingredient.get_unit(), 'g')

        ingredient = Ingredient.objects.create(name='TEST3', amount='1,1 G')
        ingredient.save()
        ingredient = Ingredient.objects.get(name='TEST3')
        self.assertEqual(ingredient.get_amount(), '1.1')
        self.assertEqual(ingredient.get_unit(), 'g')

    def test_str(self):
        ingredient = Ingredient.objects.get(name='Ingredient')
        self.assertEqual(ingredient.__str__(), 'Ingredient')

    def test_verbose(self):
        ingredient = Ingredient.objects.get(name="Ingredient")
        self.assertEqual(ingredient._meta.verbose_name, 'Ingredient')
        self.assertEqual(ingredient._meta.verbose_name_plural, 'Ingredients')


class FoodplanTestCase(TestCase):
    def setUp(self):
        pass

    def test_foodplan_save(self):
        food1 = Food(name="food1")
        food2 = Food(name="food2").save()

        food1.save()

        s_date = "01-02-16"
        e_date = "07-02-16"

        foodplan = Foodplan()
        foodplan.set_start_date(s_date, "%d-%m-%y")
        foodplan.set_end_date(e_date, "%d-%m-%y")
        foodplan.save()
        self.assertEqual(foodplan.name, s_date + " - " + e_date)
        self.assertEqual(foodplan.get_year(), "16")
        self.assertEqual(foodplan.get_month(), "02")

        day = Day(food=food1)
        day.set_day('01-02-16', '%d-%m-%y')
        day.save()
        foodplan.add_day(day)
        foodplan.save()

        day = Day.objects.filter(foodplan=foodplan)
        self.assertEqual(day[0].date.strftime("%d-%m-%y"), '01-02-16')


