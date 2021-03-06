from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import AccountForm, CustomUserCreationForm, LoginForm


def register_user(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"Вы уже зарегистрированы как {user.email}")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = authenticate(
                request,
                username=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password1"),
            )
            login(request, user)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["email"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    form.add_error(None, ValidationError("Этот аккаунт отключен"))
            else:
                form.add_error(None, ValidationError("Неверный email или пароль."))
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


@login_required(login_url="users:login")
def account(request):
    user = request.user
    paid_orders = user.orders.filter(payments__is_paid=True)
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data["email"]
            user.phonenumber = form.cleaned_data["phonenumber"]
            user.phonenumber = form.cleaned_data["phonenumber"]
            user.set_password(form.cleaned_data["password"])
            user.save()
    else:
        form = AccountForm()

    context = {"user": user, "paid_orders": paid_orders, "form": form}
    return render(request, "account.html", context)
