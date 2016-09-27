from django import forms
from django.forms import ModelForm, inlineformset_factory
from foodroller.models import Category, Food, Ingredient
from registration.forms import User
from django.contrib.auth.forms import AuthenticationForm

__author__ = 'stefanperndl'

DAYS_CHOICES = (
    (3, '3 Tage'),
    (4, '4 Tage'),
    (5, '5 Tage'),
    (6, '6 Tage'),
    (7, '7 Tage'),
)

class DateForm(forms.Form):
    days = forms.ChoiceField(label="Tage:", required=True, widget=forms.Select(attrs={'class': 'form-control',
                                                                        'required': True}), choices=DAYS_CHOICES)
    date = forms.DateField(label="Startdatum:", required=True, widget=forms.DateInput(attrs={'class': 'datepicker form-control'}))


class EmailForm(forms.Form):
    summary = forms.CharField(widget=forms.Textarea(attrs={'class': 'email-text'}))
    to = forms.EmailField(label="Empfaenger:")

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['summary'].label = False

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = ('slug', 'last_cooked', )

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

