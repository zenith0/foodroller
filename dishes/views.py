from django.shortcuts import render
from dishes.forms import DishForm

# Create your views here.
def index(request):

    form = DishForm
    return render(request, 'foodroller/index.html', {'form': form})

#def add(request):