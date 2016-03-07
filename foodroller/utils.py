import calendar
import django
import os
import sys
from collections import OrderedDict
import datetime

PLAN = 'plan'

ALREADY_ROLLED = 'already_rolled'

__author__ = 'stefan'


######################################## Session Utils ########################################


def get_cached_food_plan(request):
    return request.session[('%s' % PLAN)]


def get_already_rolled(request):
    return request.session[('%s' % ALREADY_ROLLED)]


def update_food_plan(request, dict_list):
    request.session[('%s' % PLAN)] = dict_list


def update_current_plan(request, food, day):
        dict_list = get_cached_food_plan(request)
        dict_list[:] = [d for d in dict_list if d['day'] != day]
        dict_list.append({"day": day,
                          "food": food.name})
        update_food_plan(request, dict_list)


def update_already_rolled(request, already_rolled):
    request.session[('%s' % ALREADY_ROLLED)] = already_rolled


def get_food_from_cached_plan(request):
    dict_list = get_cached_food_plan(request)
    food_list = []
    for d in dict_list:
        food_list.append(d['food'])
    return food_list


def new_already_rolled(request):
    already_rolled = get_food_from_cached_plan(request)
    update_already_rolled(request, already_rolled)
    return already_rolled

######################################## Date Utils ########################################

# Get the weekday as string from a given date
def weekday_from_date(date):
    return calendar.day_name[date.weekday()]


# Get the end date of a time period
def get_end_date(start_date, num_days):
    return start_date + datetime.timedelta(days=num_days-1)


# Create a dictionary containing a time period in the format: {'Tuesday': 23.02.1987, 'Wednesday': 24.02.1987,... }
def create_days_dict(start_date, num_days):
    days_in_row = [{start_date: weekday_from_date(start_date)}]
    for x in range(1, num_days):
        next_day = start_date + datetime.timedelta(days=x)
        days_in_row.append({next_day: weekday_from_date(next_day)})

    return days_in_row


######################################## Food Utils ########################################

# Returns a of food filtered by the given duration key (1,2,3,4,None)
def filter_food_by_duration(food_list, duration):
    if duration == "1":
        cooking_time = datetime.timedelta(minutes=30)
        food_list = food_list.filter(duration__lt=cooking_time)
    elif duration == "2":
        cooking_time = datetime.timedelta(hours=1)
        food_list = food_list.filter(duration__lt=cooking_time)
    elif duration == "3":
        cooking_time = datetime.timedelta(hours=2)
        food_list = food_list.filter(duration__lt=cooking_time)
    elif duration == "4":
        cooking_time = datetime.timedelta(hours=2)
        food_list = food_list.filter(duration__gte=cooking_time)

    return food_list


def filter_food_by_category_name(cat):
    from foodroller.models import Category
    category = Category.objects.get(name=cat)
    return category.get_food()


# Returns a dictionary with all categories as keys and its foods as their values
def category_food_dict():
    from foodroller.models import Category
    category_list = Category.objects.all()
    cat_dict = OrderedDict()
    for cat in category_list:
        cat_dict[cat] = cat.get_food()
    cat_dict = {"categories": cat_dict}
    return cat_dict


# Method to return random food
def random_food(request, cat, time, day):
    # It is necessary to hold 2 caches:
    # already_rolled: holds all food that has been ever rolled (this is needed if you want to re-roll)
    # already_rolled is reset if it is full
    already_rolled = get_already_rolled(request)
    # cached_food: holds all desired food for the rolling week - if this cache is not present we would always bring up
    # the same 2 results if a certain day is re-rolled
    cached_food = get_food_from_cached_plan(request)

    food_list = filter_food_by_category_name(cat).order_by('-last_cooked')
    food_filtered = filter_food_by_duration(food_list, time)

    food = None

    for f in food_filtered:
        if f.name not in already_rolled and f.name not in cached_food:
            already_rolled.append(f.name)
            update_current_plan(request, f, day)
            request.session['already_rolled'] = already_rolled
            food = f
            break
        # in this case all available food have been rolled --> reset the cache and fill in the day cache items
        elif len(already_rolled) >= len(food_filtered):
            already_rolled = new_already_rolled(request)

    return food