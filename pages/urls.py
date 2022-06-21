from django.urls import path

from . import views


app_name = "pages"

urlpatterns = [
    path("prices", views.prices, name="prices"),
    path("storage-rules", views.storage_rules, name="storage-rules"),
    path("addresses", views.addresses, name="addresses"),
    path("testimonials", views.testimonials, name="testimonials"),
    path("legal", views.legal, name="legal"),
    path("contacts", views.contacts, name="contacts"),
]
