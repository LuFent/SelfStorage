from django import forms

from .models import CalcRequest, Order


class CalcRequestForm(forms.ModelForm):
    class Meta:
        model = CalcRequest
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': (
                        'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 '
                        'SelfStorage__bg_lightgrey'
                    ),
                    'placeholder': 'Укажите ваш e-mail',
                }
            )
        }


class OrderForm(forms.ModelForm):
    term = forms.IntegerField(label="Срок аренды")
    class Meta:
        model = Order
        fields = ('lease_start',)




