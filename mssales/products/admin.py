from django.contrib import admin

from core.admin import SoftDeleteAdmin
from products.models import Product


@admin.register(Product)
class ProductAdmin(SoftDeleteAdmin):
    ordering = ["-created_at"]
    list_display = ("id", "name", "created_at")
    readonly_fields = ("sales_price",)
    sortable_by = ("created_at", "sales_price")
    list_per_page = 20
    search_fields = ("name",)
