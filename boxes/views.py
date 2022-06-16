from django.shortcuts import render
from django.http import HttpResponse

from users.forms import LoginForm, CustomUserCreationForm

def index(request):
    context = {
        'login_form': LoginForm(),
        'registration_form': CustomUserCreationForm(),
    }
    return render(request, 'main.html', context)


def boxes(request):
    cotext = {}
    #TODO шаблонизировать склады
    # ...
    return render(request, 'boxes.html', cotext)


def lk(request):
    return render(request, 'my-rent.html')





