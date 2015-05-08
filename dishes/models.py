from django.db import models


# Create your models here.
class Dish(models.Model):
    title = models.CharField(max_length=50)
    last_cooked = models.DateField('last time cooked')
    image = models.ImageField
    vegetarian = models.BooleanField
    recipe = models.OneToOneField('Recipe')
    cooking_time = models.TimeField('cooking time')

    def __str__(self):
        return self.title

    def last_time_cooked(self):
        return self.last_cooked

    def time_needed(self):
        return self.cooking_time


class Recipe(models.Model):
    recipe = models.CharField(max_length=2000)
    ingredients = models.ForeignKey('Ingredient')


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=50)

    def __str__(self):
        return self.ingredient