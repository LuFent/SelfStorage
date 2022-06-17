from django.urls import path

from . import views


urlpatterns = [
    path("<int:order_id>/", views.send_qr, name="send_qr"),
]
