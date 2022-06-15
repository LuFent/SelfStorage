from django.urls import path

from . import views

urlpatterns = [
    path("<int:order_id>/", views.payment, name="payment"),
    path(
        "complete/<int:order_id>/",
        views.complete_payment,
        name="complete_payment",
    ),
]
