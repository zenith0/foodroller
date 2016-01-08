from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import Model

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
    categories = models.ManyToManyField('Category', related_name='food')
    recipe = models.TextField(blank=True, null=True)
    duration = models.TimeField(null=True, blank=True)
    last_cooked = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to="img", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'

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
    food = models.ForeignKey(Food, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'