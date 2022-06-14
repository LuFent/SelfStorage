from django.contrib import admin
from boxes.models import Storage, Box


@admin.register(Box)
class OrderBox(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = "Boxes"


@admin.register(Storage)
class OrderBox(admin.ModelAdmin):
    pass