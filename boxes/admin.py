from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from boxes.models import Box, CalcRequest, Order, Storage, StorageImage
from payment.models import Payment


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


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]
    list_display = ('id', 'box', 'lease_start', 'lease_end',
                    'customer', 'get_payment')

    @admin.display(ordering='payments__status', description='Payment')
    def get_payment(self, obj):
        if obj.payments.first():
            return obj.payments.first().status


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
