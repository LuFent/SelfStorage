from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def boxes(request):
    cotext = {}
    #TODO шаблонизировать склады
    # ...
    return render(request, 'boxes.html', cotext)


def lk(request):
    return render(request, 'my-rent.html')





