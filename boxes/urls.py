from django.contrib import admin
from .views import *
from django.urls import path
from django.shortcuts import render


app_name = "boxes"

urlpatterns = [
    path('', index),
    path('faq', lambda response: render(response, 'faq.html')), #FIXME Костыль, но забыл как правильно :)
    path('boxes/<int:storage_id>', boxes, name='boxes'),
    path('lk', lk),
    path('calc-request/', handle_calc_request, name='calc-request'),
    path('orderbox/<int:box_id>', order_box, name='order-box')    
]



