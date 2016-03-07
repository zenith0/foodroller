from django.contrib import admin
from django.contrib.auth.models import User, Group
from foodroller.models import Category, Food, Ingredient

__author__ = 'stefan'

class IngredientsInline(admin.TabularInline):
    model = Ingredient


class FoodAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [IngredientsInline, ]
    exclude = ['last_cooked',]
    list_display = ('name', 'duration')


admin.site.register(Category)
admin.site.register(Food, FoodAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
