from django.db import models

from products.models import ProductVariant


class InventoryTransaction(models.Model):
    """
    Every stock movement is stored here.
    """

    PURCHASE = "PURCHASE"
    SALE = "SALE"
    RETURN = "RETURN"
    DAMAGE = "DAMAGE"
    ADJUSTMENT = "ADJUSTMENT"

    TRANSACTION_TYPES = (
        (PURCHASE, "Purchase"),
        (SALE, "Sale"),
        (RETURN, "Return"),
        (DAMAGE, "Damage"),
        (ADJUSTMENT, "Adjustment"),
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory_transactions",
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
    )

    quantity = models.IntegerField()

    note = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "inventory_transactions"
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return (
            f"{self.variant.sku} - "
            f"{self.transaction_type} "
            f"({self.quantity})"
        )