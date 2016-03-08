import datetime
import json
import re
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from foodroller.forms import DateForm, EmailForm
from foodroller.models import Category, Food
from foodroller.utils import weekday_from_date, filter_food_by_duration, create_days_dict, get_end_date, \
    category_food_dict, update_current_plan, random_food, get_cached_food_plan


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


def summary(request):
    food_plan = get_cached_food_plan(request)
    ingredients_list = []
    message = "Essensplan: \n"
    for item in food_plan:
        message += '\n'
        date = datetime.datetime.strptime(item['day'], '%d-%m-%y')
        message += date.strftime('%d.%m.%y')
        message += ':\t'
        message += item['food']

        food = Food.objects.get(name=item['food'])
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

    form = EmailForm(initial={'summary': message})

    return render(request, 'modals/email.html', {'email_form': form})
