__author__ = 'stefan'
from django import forms
from dishes.models import Dish, Ingredient, Recipe

class DishForm(forms.ModelForm):
    title = forms.CharField(max_length=50, help_text="Please enter the title of your dish")
    image = forms.FileField(label='Select a file', help_text='Please select a image to upload')
    recipe = forms.CharField(max_length=2000, help_text="Please enter the recipe of your dish", required=False)
    vegetarian = forms.BooleanField(label='Is vegetarian', required=False, initial=False, help_text="Is vegetarian?")
    cooking_time = forms.TimeField(label='Cooking time', help_text="Cooking time")

    class Meta:
        model = Dish
        fields = ('title', 'image', 'recipe', 'cooking_time', 'vegetarian', )