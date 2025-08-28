from django.db import models

from django_softdelete.models import SoftDeleteModel

from products.models import Order, Product
import uuid


class Customer(SoftDeleteModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=32)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class SalesOrder(SoftDeleteModel):
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]

    number = models.CharField(max_length=64, unique=True, editable=False)
    customer = models.ForeignKey(
        Customer, related_name="sales_orders", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="DRAFT")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"SO-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)


class SalesOrderLine(SoftDeleteModel):
    order = models.ForeignKey(
        SalesOrder, related_name="order_lines", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="sales_order_lines", on_delete=models.CASCADE
    )
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} ({self.qty})"


class Reservation(SoftDeleteModel):
    order = models.ForeignKey(
        Order, related_name="reservations", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def __str__(self):
        return f"Reservation: {self.qty} x {self.product.name} for Order {self.order.order_reference}"
