from django.contrib import admin
from boxes.models import Storage, Box, Order


@admin.register(Box)
class OrderBox(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = "Boxes"


@admin.register(Storage)
class OrderBox(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
