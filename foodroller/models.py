import datetime
from django.db import models
from django.db.models import Model
from django.utils.text import slugify
import re

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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Food, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'

    def get_ingredients(self):
        return Ingredient.objects.filter(food=self)

    def set_last_cooked(self, date_str, format):
        self.last_cooked = datetime.datetime.strptime(date_str, format)

    def get_last_cooked(self):
        return self.last_cooked.strftime("%d-%m-%y")

    def ingredients_as_dict(self):
        ingredients_list = []
        for ing in self.get_ingredients():
            already_in_list = False
            amount = re.findall("[-+]?\d*\.\d+|\d+", ing.amount)[0]
            unit = re.sub("[-+]?\d*\.\d+|\d+", "", ing.amount)
            amount_dict = {'amount': amount, 'unit': unit}
            ing_dict = {'ingredient': ing.name, 'amount': amount_dict}
            for saved_ing_dict in ingredients_list:
                if saved_ing_dict['ingredient'].lower() == ing.name.lower():
                    saved_amount_dict = saved_ing_dict['amount']
                    if unit.lower() == saved_amount_dict['unit'].lower():
                        saved_amount_dict['amount'] = str(float(amount) + float(saved_amount_dict['amount']))
                        already_in_list = True
            if not already_in_list:
                ingredients_list.append(ing_dict)
        return ingredients_list


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

    def date_as_string(self):
        return self.date.strftime("%d-%m-%y")

class Foodplan(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.ManyToManyField(Day)
    year = models.DateField()
    month = models.DateField()

    class Meta:
        ordering = ["start_date"]

    def add_day(self, day):
        self.days.add(day)

    def save(self, *args, **kwargs):
        self.name = self.start_date.strftime("%d-%m-%y") + " - " + self.end_date.strftime("%d-%m-%y")
        self.year = datetime.datetime.strptime(str(self.start_date.year), "%Y")
        self.month = datetime.datetime.strptime(str(self.start_date.month), "%m")
        self.slug = slugify(self.name)
        super(Foodplan, self).save(*args, **kwargs)

    def set_start_date(self, date_str, format):
        self.start_date = datetime.datetime.strptime(date_str, format)

    def set_end_date(self, date_str, format):
        self.end_date = datetime.datetime.strptime(date_str, format)

    def get_year(self):
        return self.year.strftime("%y")

    def get_month(self):
        return self.month.strftime("%m")

    def init_with_dict(self, cached_food_plan):
        days = Day.objects.filter(foodplan=self)
        days.delete()
        start_date = cached_food_plan[0]['day']
        end_date = cached_food_plan[len(cached_food_plan)-1]['day']
        self.set_start_date(start_date, "%d-%m-%y")
        self.set_end_date(end_date, "%d-%m-%y")
        self.save()

        for item in cached_food_plan:
            food_name = item['food']
            day_name = item['day']
            food = Food.objects.get(name=food_name)
            food.set_last_cooked(day_name, "%d-%m-%y")
            food.save()
            day = Day()
            day.set_day(day_name, "%d-%m-%y")
            day.food = food
            day.save()
            self.days.add(day)
        self.save()

    def get_summary(self):
        ingredients_list = []

        message = "Essensplan: \n"
        days = Day.objects.filter(foodplan=self)
        for day in days:
            message += '\n'
            message += day.date.strftime('%d.%m.%y')
            message += ':\t'
            message += day.food.name

            food = Food.objects.get(name=day.food.name)
            ingredients_list.extend(food.ingredients_as_dict())
            ingredients = food.get_ingredients()
            for ing in ingredients:
                already_in_list = False
                amount = re.findall("[-+]?\d*\.\d+|\d+", ing.amount)[0]
                unit = re.sub("[-+]?\d*\.\d+|\d+", "", ing.amount)
                amount_dict = {'amount': amount, 'unit': unit}
                ing_dict = {'ingredient': ing.name, 'amount': amount_dict}
                for saved_ing_dict in ingredients_list:
                    if saved_ing_dict['ingredient'].lower() == ing.name.lower():
                        saved_amount_dict = saved_ing_dict['amount']
                        if unit.lower() == saved_amount_dict['unit'].lower():
                            saved_amount_dict['amount'] = str(float(amount) + float(saved_amount_dict['amount']))
                            already_in_list = True
                if not already_in_list:
                    ingredients_list.append(ing_dict)

        message += "\n\n"
        message += "Einkaufsliste: "
        for ing in ingredients_list:
            ingredient = ing['ingredient']
            amount_dict = ing ['amount']
            amount = amount_dict['amount']
            unit = amount_dict['unit']
            message += "\n"
            message += ingredient
            message += "\t\t"
            message += amount + " " + unit

        return message

    def get_days(self):
        return list(Day.objects.filter(foodplan=self))
