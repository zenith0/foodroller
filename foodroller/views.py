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

