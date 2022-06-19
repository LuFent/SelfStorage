from django.urls import path

from . import views


app_name = "keystore"

urlpatterns = [
    path("<int:order_id>/", views.send_qr, name="send_qr"),
]
