from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from boxes.models import Box, CalcRequest, Order, Storage, StorageImage


class ImagesInline(SortableInlineAdminMixin, admin.TabularInline):
    model = StorageImage
    extra = 1
    fields = ("image", "preview", "number")
    readonly_fields = ("preview",)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = "Boxes"


@admin.register(Storage)
class StorageAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [ImagesInline]


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


admin.site.register(StorageImage)
