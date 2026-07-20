from django.db import models

from common.mixins import TimeStampMixin


class Payment(TimeStampMixin):
    """
    Stores payment information for an order.
    """

    PAYMENT_METHODS = (
        ("COD", "Cash on Delivery"),
        ("RAZORPAY", "Razorpay"),
        ("STRIPE", "Stripe"),
    )

    PAYMENT_STATUS = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    )

    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="payment",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="PENDING",
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"{self.order.order_number}"