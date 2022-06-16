from django.contrib import admin
from boxes.models import Storage, Box, Order, CalcRequest


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


@admin.register(CalcRequest)
class CalcRequestAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    ordering = ("-created_at",)
    list_display = (
        "created_at",
        "email",
        "status",
    )
    list_filter = (
        "created_at",
        "status",
    )
