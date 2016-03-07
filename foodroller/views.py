import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from foodroller.forms import DateForm
from foodroller.models import Category, Food, Foodplan
from foodroller.utils import weekday_from_date, filter_food_by_duration, create_days_dict, get_end_date, \
    category_food_dict, update_current_plan, random_food


# The index site (start)
def index(request):
    return render_to_response('index.html')


# The Food pane
def categories(request):
    cat_dict = category_food_dict()
    return render(request, 'categories.html', cat_dict)


# The roll pane
def roll(request):
    request.session['plan'] = []
    request.session['already_rolled'] = []
    days = 6
    start_date = datetime.date.today()
    date_form = DateForm()

    if request.method == 'POST':
        date_form = DateForm(request.POST)
        if date_form.is_valid():
            days = int(date_form.cleaned_data['days'])
            start_date = date_form.cleaned_data['date']

    days_dict = create_days_dict(start_date, days)
    end_date = get_end_date(start_date, days)

    category_list = Category.objects.all()

    return render(request, 'roll.html',
                  {'start': start_date,
                   'end': end_date,
                   'days': days_dict,
                   'categories': category_list,
                   'date_form': date_form})


# Display details for a specific food
def food_details(request, food_slug):
    food_dict = {}
    food = Food.objects.get(slug=food_slug)
    food_dict['food'] = food
    return render(request, 'food.html', food_dict)


# Returns json Data for autocomplete food-search
def search(request):
    search_qs = Food.objects.filter(name__icontains=request.GET['term'])
    results = []
    for r in search_qs:
        results.append(r.name)
    resp = json.dumps(results)

    return HttpResponse(resp, content_type='application/json')


# Set food manually for a specific day
def set_food(request):
    name = request.GET['name']
    day = request.GET['day']
    food = Food.objects.get(name=name)
    update_current_plan(request, food, day)
    return render(request, 'food-snippet.html', {'food': food})


# Set food randomly for a specific day
def roll_food(request):
    day = request.GET['day']
    time = request.GET['time']
    cat = request.GET['cat']
    food = random_food(request, cat, time, day)
    return render(request, 'food-snippet.html', {'food': food})
