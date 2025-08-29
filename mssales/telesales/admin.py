from django.contrib import admin

from core.admin import SoftDeleteAdmin
from telesales.models import Customer, SalesOrder, SalesOrderLine


READ_ONLY_FIELDS = (
    "deleted_at",
    "restored_at",
    "transaction_id",
)


class SalesOrderLines(admin.TabularInline):
    model = SalesOrderLine
    readonly_fields = (
        "deleted_at",
        "restored_at",
        "transaction_id",
        "unit_price",
        "sub_total",
    )
    extra = 0


@admin.register(SalesOrder)
class SalesOrderAdmin(SoftDeleteAdmin):
    inlines = [SalesOrderLines]
    ordering = ["-created_at"]
    list_display = (
        "number",
        "created_at",
        "order_total",
        "vat_rate",
        "status",
        "customer__name",
    )
    readonly_fields = ("order_total",)
    list_editable = ("status",)
    sortable_by = ("created_at", "order_tota")
    list_per_page = 20
    search_fields = ("customer__username", "number")


@admin.register(Customer)
class CustomerAdmin(SoftDeleteAdmin):
    list_display = (
        "id",
        "name",
        "email",
    )
    list_per_page = 20
    search_fields = ("name", "email")
