__author__ = 'stefan'
from django import forms
from dishes.models import Dish


class DishForm(forms.ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Name'}), required=True)
    image = forms.FileField(label='Select a file',
                            required=False)
    recipe = forms.CharField(max_length=2000,
                             widget=forms.Textarea(attrs={'placeholder': 'Recipe', 'cols': 78, 'rows': 15}),
                             required=False)
    ingredients = forms.CharField(max_length=2000, widget=forms.Textarea(
        attrs={'placeholder': 'Ingredients (each in new line)', 'cols': 78, 'rows': 15}),
                                  required=True)
    vegetarian = forms.BooleanField(label='Is vegetarian',
                                    required=False,
                                    initial=False,
                                    help_text="Is vegetarian?",
                                    )
    cooking_time = forms.TimeField(label='Cooking time',
                                   widget=forms.TimeInput(format='%H:%M'),
                                   required=True)

    class Meta:
        model = Dish
        fields = ('title', 'image', 'recipe', 'ingredients', 'cooking_time', 'vegetarian', )