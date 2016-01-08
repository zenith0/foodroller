from collections import OrderedDict
from django.shortcuts import render, render_to_response
from foodroller.models import Category, Food
from foodroller_project import settings


def category_food_dict():
    categories = Category.objects.all()
    cat_dict = OrderedDict()
    for cat in categories:
        cat_dict[cat] = cat.get_food()
    dict = {"categories": cat_dict}
    return dict


def index(request):
    return render_to_response('index.html')


def categories(request):
    cat_dict = category_food_dict()
    return render(request, 'categories.html', cat_dict)


def roll(request):
    return render_to_response('roll.html')


def food(request, food_slug):
    food_dict = {}
    food = Food.objects.get(slug=food_slug)
    food_dict['food'] = food
    return render(request, 'food.html', food_dict)
