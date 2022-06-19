from datetime import date
from django import forms
from django.forms.widgets import SelectDateWidget

from .models import CalcRequest, Order


class CalcRequestForm(forms.ModelForm):
    class Meta:
        model = CalcRequest
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": (
                        "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 "
                        "SelfStorage__bg_lightgrey"
                    ),
                    "placeholder": "Укажите ваш e-mail",
                }
            )
        }


class OrderForm(forms.ModelForm):
    lease_start = forms.DateField(
        label='Начальная дата',
        widget=SelectDateWidget(),
        initial=date.today
    )
    term = forms.IntegerField(label="Срок аренды, мес")

    class Meta:
        model = Order
        fields = ('id', )
