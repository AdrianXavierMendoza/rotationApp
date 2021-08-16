from .models import *
from django import forms


class BuildForm(forms.Form):
    Build_type = forms.ChoiceField(
        widget = forms.Select(), choices=Status.CREW_STATUS)
