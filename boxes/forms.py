from django import forms

from .models import CalcRequest


class CalcRequestForm(forms.ModelForm):
    class Meta:
        model = CalcRequest
        fields = ('email',)
