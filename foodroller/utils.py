import calendar
import random
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
                          "food": food})
        update_food_plan(request, dict_list)

def update_already_rolled(request, already_rolled):
    request.session[('%s' % ALREADY_ROLLED)] = already_rolled

def set_food_plan(request, food_plan):
    days = food_plan.get_days()
    dict_list = []
    for day in days:
        dict_list.append({"day": day.date_as_string(),
                          "food": day.food.name})
    update_food_plan(request, dict_list)


def get_food_from_cached_plan(request):
    dict_list = get_cached_food_plan(request)
    food_list = []
    for d in dict_list:
        food_list.append(d['food'])
    return list(set(food_list))


def new_already_rolled(request):
    already_rolled = get_food_from_cached_plan(request)
    update_already_rolled(request, already_rolled)
    return already_rolled

def clear_food_plan(request):
    request.session[('%s' % PLAN)] = []


######################################## Food Utils ########################################
# Returns a of food filtered by the given duration key (1,2,3,4,None)
def filter_food_by_duration(food_list, duration):
    filtered_food_list = []
    valid_times = []
    if duration == '30min':
        valid_times.append('30min')
    elif duration == '1hr':
        valid_times.append('30min')
        valid_times.append('1hr')
    elif duration == '2hr':
        valid_times.append('30min')
        valid_times.append('1hr')
        valid_times.append('2hr')
    elif duration == '2hr+':
        valid_times.append('2hr+')
    else:
        return food_list

    for time in valid_times:
        filtered_food_list.extend(food_list.filter(duration=time))

    if len(filtered_food_list) > 0:
        return filtered_food_list
    return food_list


def filter_food_by_category_name(cat, user):
    from foodroller.models import Category
    category = Category.objects.get(name=cat, user=user)
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


def merge_ingredients(ingredients):
        ingredients_list = []
        for ing in ingredients:
            already_in_list = False
            amount_dict = {'amount': ing.get_amount(), 'unit': ing.get_unit()}
            ing_dict = {'ingredient': ing.name, 'amount': amount_dict}
            for saved_ing_dict in ingredients_list:
                if saved_ing_dict['ingredient'].lower() == ing.name.lower():
                    saved_amount_dict = saved_ing_dict['amount']
                    if ing.get_unit() == saved_amount_dict['unit']:
                        saved_amount_dict['amount'] = str(float(ing.get_amount()) + float(saved_amount_dict['amount']))
                        already_in_list = True
            if not already_in_list:
                ingredients_list.append(ing_dict)
        return ingredients_list

def merge_ingredients_dict(ingredients):
        ingredients_list = []
        for ing in ingredients:
            already_in_list = False
            tmp = ing['amount']
            amount_dict = {'amount': tmp['amount'], 'unit': tmp['unit']}
            ing_dict = {'ingredient':ing['ingredient'], 'amount': amount_dict}
            for saved_ing_dict in ingredients_list:
                if saved_ing_dict['ingredient'].lower() == ing['ingredient'].lower():
                    saved_amount_dict = saved_ing_dict['amount']
                    if tmp['unit'] == saved_amount_dict['unit']:
                        saved_amount_dict['amount'] = str(float(tmp['amount']) + float(saved_amount_dict['amount']))
                        already_in_list = True
            if not already_in_list:
                ingredients_list.append(ing_dict)
        return ingredients_list