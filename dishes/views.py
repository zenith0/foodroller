from django.shortcuts import render
from dishes.forms import DishForm

# Create your views here.
def index(request):

    if request.method == 'POST':
        form = DishForm(request.POST)

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
    return render(request, 'foodroller/index.html', {'form': form})

def add(request):
    if request.method == 'POST':
        form = DishForm(request.POST)

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