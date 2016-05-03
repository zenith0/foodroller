from PIL import Image
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import Model
from django.utils.text import slugify
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
    duration = models.DurationField(null=True, blank=True, help_text="hh:mm:ss (01:30:00 = 1 hr 30 min)")
    last_cooked = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to="img", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'

    def get_ingredients(self):
        return Ingredient.objects.filter(food=self)


class Ingredient(models.Model):
    name = models.CharField(blank=False, max_length=50)
    amount = models.CharField(null=True, blank=True, max_length=10)
    food = models.ForeignKey(Food, null=True, blank=True, related_name='ingredient')

    def __str__(self):
        return self.name

    # prettify the amount field
    def save(self, *args, **kwargs):
        self.amount = self.amount.replace(" ", "")
        self.amount = self.amount.replace(",", ".")
        super(Ingredient, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class Day(models.Model):
    date = models.DateField()
    food = models.ForeignKey('Food')

    def save(self, *args, **kwargs):
        self.food.last_cooked = self.date
        super(Day, self).save(*args, **kwargs)

    def set_day(self, date_str, format):
        self.date = datetime.datetime.strptime(date_str, format)

    def set_food(self, food_name):
        self.food = Food.objects.get(name=food_name)


class Foodplan(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    food_list = models.ManyToManyField('Day')
    year = models.DateField()
    month = models.DateField()

    def add_food(self, day):
        self.food_list.add(day)

    def save(self, *args, **kwargs):
        self.name = self.start_date.strftime("%d.%m.%Y") + " - " + self.end_date.strftime("%d.%m.%Y")
        self.year = datetime.datetime.strptime(str(self.start_date.year), "%Y")
        self.month = datetime.datetime.strptime(str(self.start_date.month), "%Y")
        super(Foodplan, self).save(*args, **kwargs)

    def set_start_date(self, date_str, format):
        self.start_date = datetime.datetime.strptime(date_str, format)

    def set_end_date(self, date_str, format):
        self.end_date = datetime.datetime.strptime(date_str, format)
