from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from foodroller.forms import DishForm
from foodroller.models import Dish

# in the index all foodroller are shown in the slider
def index(request):
    return render(request, 'foodroller/index.html', {'list': Dish.objects.all()})


def add(request):

    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            url = reverse("index")
            return HttpResponseRedirect(url)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)

    else:
        # If the request was not a POST, display the form to enter details.
        form = DishForm()
    return render(request, 'foodroller/add.html', {'form': form})


def edit(request, dish_slug):
    if request.method == 'POST':
        print ('##########POST')
        if 'delete' in request.POST:
            print ('###########DELETE')
            dish = Dish.objects.get(slug=dish_slug)
            dish.delete()

        if 'save' in request.POST:
            print ('###########SAVE')

        url = reverse("index")
        return HttpResponseRedirect(url)

    else:
        print ('########GET')
        dish = Dish.objects.get(slug=dish_slug)
        return render(request, 'foodroller/edit.html', {'dish': dish})
