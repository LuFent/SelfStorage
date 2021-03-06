from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from .views import *


app_name = "boxes"

urlpatterns = [
    path("", index),
    path(
        "faq", lambda response: render(response, "faq.html")
    ),  # FIXME Костыль, но забыл как правильно :)
    path("boxes/<int:storage_id>", boxes, name="boxes"),
    path("boxes/", storages, name="storages"),
    path("calc-request/", handle_calc_request, name="calc-request"),
    path("orderbox/<int:box_id>", order_box, name="order-box"),
]
