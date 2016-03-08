from django import forms
from foodroller.models import Category

__author__ = 'stefanperndl'

DAYS_CHOICES = (
    (3, '3 Tage'),
    (4, '4 Tage'),
    (5, '5 Tage'),
    (6, '6 Tage'),
    (7, '7 Tage'),
)


def set_categories():
    categories = Category.objects.all()
    list = []
    for cat in categories:
        list.append(cat.name)


class DateForm(forms.Form):
    days = forms.ChoiceField(label="Tage:", required=True, widget=forms.Select(attrs={'class': 'w-select days-sel',
                                                                        'required': True}), choices=DAYS_CHOICES)
    date = forms.DateField(label="Startdatum:", required=True, widget=forms.DateInput(attrs={'class': 'datepicker'}))


class EmailForm(forms.Form):
    summary = forms.CharField(widget=forms.Textarea(attrs={'class': 'email-text'}))
    to = forms.EmailField(label="Empfaenger:")

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['summary'].label = False


