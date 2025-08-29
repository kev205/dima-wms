from django.db import models


from django_softdelete.models import SoftDeleteModel


class TimeStampedModel(SoftDeleteModel):
    created_at = models.DateTimeField(
        null=True, blank=True, auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        abstract = True
