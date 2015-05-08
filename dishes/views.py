from django.shortcuts import render
from dishes.forms import DishForm

# Create your views here.
def index(request):
    return render(request, 'foodroller/index.html')


def add(request):
    form = DishForm
    return render(request, 'foodroller/add.html', {'form': form})