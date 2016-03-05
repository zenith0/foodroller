import datetime
import json

from collections import OrderedDict
from django.core import serializers
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from foodroller import utils
from foodroller.models import Category, Food, Foodplan
from foodroller_project import settings
from foodroller.utils import weekday_from_date


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
    request.session['plan'] = []
    request.session['already_rolled'] = []

    try:
        days = int(request.GET['days'])
    except:
        days = 6
    try:
        date = request.GET['date']
        starting_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except:
        starting_date = datetime.date.today()

    foodplan = Foodplan.objects.all()
    end_date = starting_date + datetime.timedelta(days=days-1)
    days_in_row=[]
    days_in_row.append({starting_date: weekday_from_date(starting_date)})
    for x in range(1, days):
        next_day = starting_date + datetime.timedelta(days=x)
        days_in_row.append({next_day: weekday_from_date(next_day)})
    categories = Category.objects.all()

    return render(request, 'roll.html',
                  {'start': starting_date,
                   'end': end_date,
                   'days': days_in_row,
                   'categories': categories})


def food(request, food_slug):
    food_dict = {}
    food = Food.objects.get(slug=food_slug)
    food_dict['food'] = food
    return render(request, 'food.html', food_dict)


def search(request):
    search_qs = Food.objects.filter(name__icontains=request.GET['term'])
    results = []
    for r in search_qs:
        results.append(r.name)
    # resp = request.GET['callback'] + '(' + json.dumps(results) + ');'
    resp = json.dumps(results)

    return HttpResponse(resp, content_type='application/json')


def search_food(request):
    name = request.GET['name']
    day = request.GET['day']
    food = Food.objects.get(name=name)
    dict_list = request.session['plan']
    dict_list[:] = [d for d in dict_list if d['day'] != day]
    dict_list.append({"day": day,
                      "food": food.name})
    request.session['plan'] = dict_list
    return render(request, 'food-snippet.html', {'food': food})

def random_food(request, cat, time, day):
    dict_list = []
    cached_food = []
    already_rolled = request.session['already_rolled']

    category = Category.objects.get(name=cat)
    food_list = category.get_food().order_by('-last_cooked')
    # food_list = Food.objects.filter(categories=category).order_by('-last_cooked')
    if time == "1":
        cooking_time = datetime.timedelta(minutes=30)
        food_filtered = food_list.filter(duration__lt=cooking_time)
    elif time == "2":
        cooking_time = datetime.timedelta(hours=1)
        food_filtered = food_list.filter(duration__lt=cooking_time)
    elif time == "3":
        cooking_time = datetime.timedelta(hours=2, minutes=1)
        food_filtered = food_list.filter(duration__lt=cooking_time)
    elif time == "4":
        cooking_time = datetime.timedelta(hours=2)
        food_filtered = food_list.filter(duration__gt=cooking_time)
    else:
        food_filtered = food_list

    try:
        dict_list = request.session['plan']
        for dict in dict_list:
            cached_food.append(dict['food'])
    except:
        request.session['plan'] = []
    food = None
    for f in food_filtered:
        if f.name not in already_rolled and f.name not in cached_food:
            already_rolled.append(f.name)
            dict_list[:] = [d for d in dict_list if d['day'] != day]

            dict_list.append({"day": day,
                              "food": f.name})
            request.session['plan'] = dict_list
            request.session['already_rolled'] = already_rolled
            food = f
            break
        # in this case all available food have been rolled --> reset the cache and fill in the day cache items
        elif len(already_rolled) == len(food_filtered):
            already_rolled.clear()
            already_rolled.extend(cached_food)
    return food

def roll_food(request):
    day = request.GET['day']
    time = request.GET['time']
    cat = request.GET['cat']
    food = random_food(request, cat, time, day)
    return render(request, 'food-snippet.html', {'food': food})
