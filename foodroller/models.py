from PIL import Image
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import Model
from foodroller.utils import weekday_from_date

__author__ = 'stefan'


class Category(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_food(self):
        return self.food.all()


class Food(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=50)
    slug = models.SlugField(unique=True, blank=False, null=False)
    categories = models.ManyToManyField('Category', related_name='food')
    recipe = models.TextField(blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    last_cooked = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to="img", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'

    def get_ingredients(self):
        return Ingredient.objects.filter(food=self)

    #def save(self, *args, **kwargs):
    #    if self.img:
    #        super(Food, self).save(*args, **kwargs)
    #        image = Image.open(self.img)
    #        size = (400, 400)
    #        path = self.img.path
    #        self.img = image.resize(size, Image.ANTIALIAS)
    #        self.img.save(path)
    #    super(Food, self).save(*args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField(blank=False, max_length=50)
    amount = models.CharField(null=True, blank=True, max_length=10)
    food = models.ForeignKey(Food, null=True, blank=True, related_name='ingredient')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

class Day(models.Model):
    food = models.ForeignKey('Food')
    date = models.DateTimeField()
    #day = weekday_from_date(datetime.datetime(date.year, date.month, date.day))


class Foodplan(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    food_list = models.ManyToManyField('Day')

    def add_food(self, food, date):
        plan_item = Day(food=food, date=date)
        self.end_date = date
        self.food_list.add(plan_item)