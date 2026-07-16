from django.db import models


class TimeStampMixin(models.Model):
    """
    Adds created_at and updated_at fields
    to every model that inherits it.
    """

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True