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


