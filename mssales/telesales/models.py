from django.db import models

from django_softdelete.models import SoftDeleteModel

from core.models import TimeStampedModel
from products.models import Product
import uuid


class Customer(SoftDeleteModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=32)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class SalesOrder(TimeStampedModel):
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]

    number = models.CharField(max_length=64, unique=True, editable=False)
    customer = models.ForeignKey(
        Customer, related_name="sales_orders", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default="DRAFT", db_index=True
    )
    notes = models.TextField(blank=True, null=True)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"SO-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)


class SalesOrderLine(TimeStampedModel):
    order = models.ForeignKey(
        SalesOrder, related_name="lines", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="sales_order_lines", on_delete=models.CASCADE
    )
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} ({self.qty})"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.unit_price = self.product.sales_price
            self.sub_total = self.qty * self.unit_price * (1 - self.discount_pct / 100)
        super().save(*args, **kwargs)


class Reservation(TimeStampedModel):
    order = models.ForeignKey(
        SalesOrder, related_name="reservations", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def __str__(self):
        return f"Reservation: {self.qty} x {self.product.name} for Order {self.order.number}"
