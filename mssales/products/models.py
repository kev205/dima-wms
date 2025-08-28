from django.db import models

from django_softdelete.models import SoftDeleteModel

from suppliers.models import Vendor

# Create your models here.


class Product(SoftDeleteModel):
    favorite = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    internal_reference = models.CharField(max_length=64, blank=True, null=True)
    responsible = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=64, blank=True, null=True)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    product_category = models.CharField(max_length=255)
    product_type = models.CharField(max_length=64)
    quantity_on_hand = models.IntegerField()
    forecasted_quantity = models.IntegerField()
    activity_exception_decoration = models.CharField(
        max_length=255, blank=True, null=True
    )


class Order(SoftDeleteModel):
    PRIORITY_CHOICES = [
        ("Normal", "Normal"),
    ]
    STATUS_CHOICES = [
        ("Purchase Order", "Purchase Order"),
        ("RFQ", "RFQ"),
        ("RFQ Sent", "RFQ Sent"),
        ("Cancelled", "Cancelled"),
        ("Locked", "Locked"),
    ]

    priority = models.CharField(max_length=32, choices=PRIORITY_CHOICES)
    order_reference = models.CharField(max_length=64, unique=True)
    vendor = models.ForeignKey(Vendor, related_name="orders", on_delete=models.CASCADE)
    purchase_representative = models.CharField(max_length=255)
    order_deadline = models.DateTimeField()
    activities = models.CharField(max_length=255, blank=True, null=True)
    source_document = models.CharField(max_length=255, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return self.order_reference


class OrderLine(SoftDeleteModel):
    order = models.ForeignKey(
        Order, related_name="order_lines", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_unit = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
