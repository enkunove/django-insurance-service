from django.contrib import admin

from .models import Promocode


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ["secret_string", "discount_type", "amount", "is_active"]
    search_fields = ["amount", "discount_type"]
    list_filter = ["is_active", "discount_type"]
    readonly_fields = ["created_at", ]
    list_per_page = 10
