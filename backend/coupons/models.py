from django.db import models
from django.utils import timezone

from common.mixins import TimeStampMixin


class Coupon(TimeStampMixin):
    """
    Coupon Model.
    """

    PERCENTAGE = "PERCENTAGE"
    FLAT = "FLAT"

    DISCOUNT_TYPES = (
        (PERCENTAGE, "Percentage"),
        (FLAT, "Flat"),
    )

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPES,
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    usage_limit = models.PositiveIntegerField(
        default=0,
        help_text="0 = Unlimited",
    )

    used_count = models.PositiveIntegerField(
        default=0,
    )

    valid_from = models.DateTimeField()

    valid_until = models.DateTimeField()

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "coupons"

        ordering = [
            "-created_at",
        ]

    def is_valid(self):
        """
        Check whether the coupon is currently valid.
        """

        now = timezone.now()

        if not self.is_active:
            return False

        if now < self.valid_from:
            return False

        if now > self.valid_until:
            return False

        if (
            self.usage_limit != 0
            and self.used_count >= self.usage_limit
        ):
            return False

        return True

    def __str__(self):
        return self.code