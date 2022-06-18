from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from .models import User


FORM_FIELD_STYLES = (
    "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 " "SelfStorage__bg_lightgrey"
)
ACCOUNT_FORM_FIELD_STYLES = "form-control fs_24 ps-2 SelfStorage__input"


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": FORM_FIELD_STYLES, "placeholder": "E-mail"}
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": FORM_FIELD_STYLES, "placeholder": "Имя", "required": False}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": FORM_FIELD_STYLES,
                "placeholder": "Фамилия",
                "required": False,
            }
        )
    )
    phonenumber = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "class": FORM_FIELD_STYLES,
                "placeholder": "Телефон",
                "required": False,
            }
        )
    )
    avatar = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": FORM_FIELD_STYLES,
                "placeholder": "Аватарка",
                "required": False,
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": FORM_FIELD_STYLES, "placeholder": "Пароль"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": FORM_FIELD_STYLES, "placeholder": "Подтверждение пароля"}
        )
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phonenumber",
            "avatar",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            User.objects.get(email=email)
        except Exception:
            return email
        raise forms.ValidationError(f"E-mail {email} уже существует.")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": FORM_FIELD_STYLES, "placeholder": "E-mail"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": FORM_FIELD_STYLES, "placeholder": "Пароль"}
        )
    )


class AccountForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": ACCOUNT_FORM_FIELD_STYLES, "disabled": True}
        )
    )
    phonenumber = PhoneNumberField(
        widget=forms.TextInput(
            attrs={"class": ACCOUNT_FORM_FIELD_STYLES, "disabled": True}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": ACCOUNT_FORM_FIELD_STYLES, "disabled": True}
        )
    )
