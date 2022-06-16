from django.shortcuts import render, redirect
from django.http import HttpResponse

from users.forms import LoginForm, CustomUserCreationForm
from boxes.forms import CalcRequestForm

def index(request):
    context = {
        'login_form': LoginForm(),
        'registration_form': CustomUserCreationForm(),
        'calc_request_form': CalcRequestForm(),
    }
    return render(request, 'main.html', context)


def boxes(request):
    cotext = {}
    #TODO шаблонизировать склады
    # ...
    return render(request, 'boxes.html', cotext)


def lk(request):
    return render(request, 'my-rent.html')


def handle_calc_request(request):
    if request.method == 'POST':
        form = CalcRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Менеджер ответит вам в течение часа.')
    else:
        form = CalcRequestForm()
    return render(request, 'users/register.html', {'form': form})



