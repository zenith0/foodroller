from django.contrib import admin
from foodroller.models import Category, Food, Ingredient

__author__ = 'stefan'

class IngredientsInline(admin.TabularInline):
    model = Ingredient


class FoodAdmin(admin.ModelAdmin):
    inlines = [IngredientsInline, ]
    exclude = ['last_cooked',]


admin.site.register(Category)
admin.site.register(Food, FoodAdmin)
