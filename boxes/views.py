from django.shortcuts import render
from django.http import HttpResponse

from users.forms import LoginForm

def index(request):
    context = {'login_form': LoginForm()}
    return render(request, 'index.html', context)


def boxes(request):
    cotext = {}
    #TODO шаблонизировать склады
    # ...
    return render(request, 'boxes.html', cotext)


def lk(request):
    return render(request, 'my-rent.html')





