from django.conf import settings
from django.db import models

from common.mixins import TimeStampMixin

from products.models import ProductVariant

class Cart(TimeStampMixin):
    """
    Shopping cart for a user.

    Each user has one active cart.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    class Meta:
        db_table = "carts"

    def __str__(self):
        return f"{self.user.email}'s Cart"


class CartItem(TimeStampMixin):
    """
    Items inside a shopping cart.
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    price_at_added = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        db_table = "cart_items"

        unique_together = (
            "cart",
            "variant",
        )

    def __str__(self):
        return (
            f"{self.variant.sku} x {self.quantity}"
        )