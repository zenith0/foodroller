import datetime
import json
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.forms import inlineformset_factory
from operator import itemgetter
import os
import random
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView
from foodroller.commons.date_utils import Date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from foodroller.forms import DateForm, EmailForm, CategoryForm, FoodForm
from foodroller.models import Category, Food, Foodplan, Day, Ingredient
from foodroller.utils import update_current_plan, get_cached_food_plan, \
    get_food_from_cached_plan, filter_food_by_category_name, filter_food_by_duration, clear_food_plan, set_food_plan

# The index site (start)
class FoodPreview(ListView):
    model = Day
    template_name = 'index.html'
    context_object_name = 'next_days'

    def get_next_days(self, number_days):
        foodplan_list = Foodplan.objects.filter(end_date__gte=datetime.date.today()).order_by('end_date')
        next_days = []
        cnt = 0
        try:
            for foodplan in foodplan_list:
                days = Day.objects.filter(foodplan=foodplan).order_by('date')
                for day in days:

                    if cnt >= number_days:
                        raise Exception
                    if day.date >= datetime.date.today():
                        cnt += 1
                        next_days.append(day)
        except Exception:
            pass
        return next_days

    def get_queryset(self):
        return self.get_next_days(6)

class Categories(ListView):

    template_name = 'food-main.html'
    context_object_name = 'categories'
    model = Category

class CategoryDetails(ListView):
    model = Food
    context_object_name = 'food'
    template_name = 'category-details.html'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return category.get_food()


class CreateCategory(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'

class DeleteCategory(DeleteView):
    model = Category
    success_url = reverse_lazy('manage')

    def get(self, request, *args, **kwargs):
        return self.post(self, request, args, kwargs)

class DeleteFood(DeleteView):
    model = Food
    success_url = ''

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        cat_slug = kwargs['cat_slug']
        food = Food.objects.get(slug=slug)
        category = Category.objects.get(slug=cat_slug)
        self.success_url = '/manage/category/' + category.slug
        return self.post(self, request, args, kwargs)

class UpdateCategory(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'manage-category.html'
    success_url = reverse_lazy('manage')

    def get(self, request, *args, **kwargs):
        slug=self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        data = {'name' : category.name, 'slug' : category.slug}
        form = CategoryForm(initial=data)
        return render(request, self.template_name, {'categories':Category.objects.all(),
                                                    'form': form})



# The roll pane
class RollView(View):
    food_list = False
    start_date = datetime.date.today()
    date_form = DateForm()
    days = 6
    days_dict = Date.create_days_dict(start_date, days)
    end_date = Date.get_end_date(start_date, days)
    category_list = Category.objects.all()
    template = 'roll-config.html'

    def init_with_start_end_date(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        time_diff = self.end_date - self.start_date
        self.days = int(time_diff.days) + 1
        self.days_dict = Date.create_days_dict(self.start_date, self.days)
        self.end_date = Date.get_end_date(self.start_date, self.days)

    @staticmethod
    def send_response(self, request):
        return render(request, 'roll.html',
                      {'start': self.start_date,
                       'end': self.end_date,
                       'days': self.days_dict,
                       'categories': self.category_list,
                       'date_form': self.date_form,
                       'food_list': self.food_list,
                       'template': self.template,
                       'times': Food.COOKING_TIMES})

    def get(self, request):
        clear_food_plan(request)
        return self.send_response(self, request)

    def post(self, request):
        date_form = DateForm(request.POST)
        if date_form.is_valid():
            self.days = int(date_form.cleaned_data['days'])
            self.start_date = date_form.cleaned_data['date']
            self.end_date = self.start_date + datetime.timedelta(self.days - 1)
            self.init_with_start_end_date(self.start_date, self.end_date)
        return self.send_response(self, request)

class FoodDetails(DetailView):

    model = Food
    template_name = 'food.html'
    context_object_name = 'food'

# Returns json Data for autocomplete food-search

class SearchFood(View):

    def get(self, request):
        s = request.GET['term']
        if len(s) < 3:
            return
        search_qs = Food.objects.filter(name__icontains=request.GET['term'])
        results = []
        for r in search_qs:
            results.append(r.name)
            resp = json.dumps(results)
        return HttpResponse(resp, content_type='application/json')

    def post(self, request):
        name = request.POST['name']
        day = request.POST['day']
        food = Food.objects.get(name=name)
        update_current_plan(request, food.name, day)
        return render(request, 'food-snippet.html', {'food': food})


# Set food randomly for a specific day
class RollFood(View):

    @staticmethod
    def random_food(request, cat, time, day):
        cached_food = get_food_from_cached_plan(request)

        food_list = filter_food_by_category_name(cat).order_by('last_cooked')
        food_filtered = filter_food_by_duration(food_list, time)

        food = random.choice(food_filtered)
        food_filtered = food_filtered.exclude(slug=food.slug)

        while len(food_filtered) > 0 and food.name in cached_food:
            food = random.choice(food_filtered)
            food_filtered = food_filtered.exclude(slug=food.slug)

        update_current_plan(request, food.name, day)
        return food

    def get(self, request):
        day = request.GET['day']
        time = request.GET['time']
        cat = request.GET['cat']
        food = self.random_food(request, cat, time, day)
        return render(request, 'food-snippet.html', {'food': food})


class SummaryView(View):
    def get(self, request):
        foodplan_list = get_cached_food_plan(request)
        ordered_food_plan = sorted(foodplan_list, key=itemgetter('day'))
        try:
            food_plan = Foodplan.objects.get(start_date=datetime.datetime.strptime(
                ordered_food_plan[0]['day'], "%d-%m-%y"))
        except ObjectDoesNotExist:
            food_plan = Foodplan()
        food_plan.init_with_dict(ordered_food_plan)
        summary = food_plan.get_summary()

        form = EmailForm(initial={'summary': summary})
        return render(request, 'modals/email.html', {'email_form': form})

    def post(self, request):
        clear_food_plan(request)
        return redirect('/plans')


class Plans(ListView):
    template_name = 'plans.html'
    context_object_name = 'plans'
    model = Foodplan


class PlanDetails(RollView):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        foodplan = Foodplan.objects.get(slug=slug)
        set_food_plan(request, foodplan)
        self.init_with_start_end_date(start_date=foodplan.start_date, end_date=foodplan.end_date)
        self.days_dict = foodplan.get_days()
        self.food_list = True
        self.template = 'roll-update.html'
        return self.send_response(self, request)


def delete_details(request, slug):
    foodplan_list = Foodplan.objects.filter(slug=slug)
    for foodplan in foodplan_list:
        foodplan.delete()

    menu = Foodplan.objects.all().order_by('-start_date')
    return render(request, 'plans.html', {'menu': menu})

class ManageCategories(Categories):
    template = 'manage-category.html'
    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        return render(request, self.template, {'categories':Category.objects.all(),
                                               'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError as e:
                return render(request, self.template, {'categories':Category.objects.all(),
                                               'form': CategoryForm()})
        else: #invalid case
            print (form.is_valid())   #form contains data and errors
            print (form.errors)
            return render(request, self.template, {'categories':Category.objects.all(),
                                                   'form': form})

        return render(request, self.template, {'categories':Category.objects.all(),
                                               'form': CategoryForm()})

class ManageFood(ListView):
    template = 'manage-food.html'
    ingredientFormSet = inlineformset_factory(Food, Ingredient,
                                              can_delete=False,
                                              extra=5,
                                              fields=('name', 'amount'))
    form = FoodForm()
    category = None

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        self.category = Category.objects.get(slug=slug)
        ingredient_formset = self.ingredientFormSet(instance=Food())
        return render(request, self.template, {'food':self.category.get_food(),
                                               'form': FoodForm(initial={'categories': [self.category]}),
                                               'ingredient_formset': ingredient_formset,
                                               'category': self.category})

    def post(self, request, *args, **kwargs):
        ingredient_form_set = None
        form = FoodForm(request.POST, request.FILES or None)
        category_slug = os.path.basename(os.path.normpath(request.path_info))
        self.category = Category.objects.get(slug=category_slug)
        if form.is_valid():
            try:
                food = form.save()

                ingredient_form_set = self.ingredientFormSet(request.POST, instance=food)
                ingredient_form_set.save()
                form = self.form
                ingredient_form_set = self.ingredientFormSet
            except IntegrityError as e:
                print('Integrity error: ' + str(e))

        return render(request, self.template, {'food':self.category.get_food(),
                                               'form': form,
                                               'ingredient_formset': ingredient_form_set,
                                               'category': self.category})


class UpdateFood(UpdateView):
    model = Food
    template = 'manage-food.html'
    success_url = reverse_lazy('manage')
    IngredientFormSet = inlineformset_factory(Food, Ingredient,
                                              can_delete=True,
                                              extra=5,
                                              fields=('name', 'amount'))
    food = None

    def get(self, request, *args, **kwargs):
        slug=self.kwargs['slug']
        cat_slug=self.kwargs['cat_slug']
        food = Food.objects.get(slug=slug)
        category = Category.objects.get(slug=cat_slug)
        form = FoodForm(instance=food)
        ingredientFormSet = self.IngredientFormSet(instance=food)

        return render(request, self.template, {'food':category.get_food(),
                                               'form': form,
                                               'ingredient_formset': ingredientFormSet,
                                               'category': category})

    def post(self, request, *args, **kwargs):
        food = Food.objects.get(slug=self.kwargs['slug'])
        form = FoodForm(request.POST, request.FILES or None, instance=food)
        ingredient_form_set = self.IngredientFormSet(request.POST, instance=food)
        category_slug = self.kwargs['cat_slug']
        category = Category.objects.get(slug=category_slug)
        if form.is_valid():
            try:
                form.save()
                ingredient_form_set.save()
                form = FoodForm(initial={'categories': [category]})
                ingredient_form_set = self.IngredientFormSet
            except IntegrityError as e:
                print('Integrity error: ' + str(e))

        return render(request, self.template, {'food': category.get_food(),
                                               'form': form,
                                               'ingredient_formset': ingredient_form_set,
                                               'category': category})