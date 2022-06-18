from django.contrib import admin

from .models import BoxKey


@admin.register(BoxKey)
class OrderAdmin(admin.ModelAdmin):
    pass
