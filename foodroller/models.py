from django.db import models
from PIL import Image

# Create your models here.
from django.template.defaultfilters import slugify


class Dish(models.Model):
    title = models.CharField(max_length=50, default='', primary_key=True)
    last_cooked = models.DateField('last time cooked', default='1970-01-01')
    image = models.ImageField(upload_to='photo', default='photo/Braten.jpg')
    vegetarian = models.BooleanField(default=False)
    cooking_time = models.TimeField('cooking time', default='')
    recipe = models.CharField(max_length=2000, default='')
    ingredients = models.CharField(max_length=2000, default='')
    slug = models.SlugField(unique=True, default='')

    def __str__(self):
        return self.title

    def last_time_cooked(self):
        return self.last_cooked

    def time_needed(self):
        return self.cooking_time

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Dish, self).save(*args, **kwargs)
