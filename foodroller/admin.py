from django.contrib import admin
from foodroller.models import Category

__author__ = 'stefan'


class CategoryAdmin(admin.ModelAdmin):

    class Meta:
        model = Category

admin.site.register(Category)

