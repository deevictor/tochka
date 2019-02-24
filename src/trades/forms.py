import datetime

from django import forms
# from django.contrib.admin.widgets import AdminDateWidget
from django.forms import DecimalField


class DatesForm(forms.Form):
    date_from = forms.DateField(
        initial=datetime.date.today, widget=forms.SelectDateWidget,
        required=False
    )

    date_to = forms.DateField(
        initial=datetime.date.today, widget=forms.SelectDateWidget,
        required=False
    )


VALUE_CHOICES = [
    ('open', 'open value'),
    ('high', 'high value'),
    ('low', 'low value'),
    ('close', 'close value'),
    ]


class DeltaForm(forms.Form):
    value = DecimalField(max_digits=5, decimal_places=2, required=False)
    type = forms.CharField(
        label='choose the value for delta',
        widget=forms.Select(choices=VALUE_CHOICES),
        required=False
    )
