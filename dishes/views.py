from django.shortcuts import render
from dishes.forms import DishForm
from dishes.models import Dish

# in the index all dishes are shown in the slider
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
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors

    else:
        # If the request was not a POST, display the form to enter details.
        form = DishForm()
    return render(request, 'foodroller/add.html', {'form': form})

def edit(request, dish_slug):

    dish = Dish.objects.get(slug=dish_slug)
    return render(request, 'foodroller/edit.html', {'dish': dish})