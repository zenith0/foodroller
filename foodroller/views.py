import datetime
import json

from collections import OrderedDict
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
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

    print (resp)
    return HttpResponse(resp, content_type='application/json')


def search_food(request):
    name = request.GET['name']
    food = Food.objects.get(name=name)
    return render(request, 'food-snippet.html', {'food': food})


def roll_food(request):
    day = request.GET['day']
    time = request.GET['time']
    cat = request.GET['cat']

    category = Category.objects.get(name=cat)
    food_list = category.get_food()

    if time == "1":
        cooking_time = datetime.datetime(0,0,0,0,31)
        food_filtered = food_list.filter(cooking_time__lt=cooking_time).order_by('-last_cooked')
    elif time == "2":
        cooking_time = datetime.datetime(0,0,0,1,1)
        food_filtered = food_list.filter(cooking_time__lt=cooking_time).order_by('-last_cooked')
    elif time == "3":
        cooking_time = datetime.datetime(0,0,0,2,1)
        food_filtered = food_list.filter(cooking_time__lt=cooking_time).order_by('-last_cooked')
    else:
        cooking_time = datetime.datetime(0,0,0,2,0)
        food_filtered = food_list.filter(cooking_time__gt=cooking_time).order_by('-last_cooked')

    cached_food = request.session['food_cache']

    for food in food_filtered:
        if not cached_food.contains(food):
            cached_food.append(food)
            request.session['food_cache'] = cached_food
            return food





    return None