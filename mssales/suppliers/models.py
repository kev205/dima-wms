from django.db import models

from django_softdelete.models import SoftDeleteModel


class Vendor(SoftDeleteModel):
    name = models.CharField(max_length=255)
    is_company = models.BooleanField(default=False)
    related_company = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="contacts",
    )
    address_type = models.CharField(max_length=64, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="ZIP"
    )
    city = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name
