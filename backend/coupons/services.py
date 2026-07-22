from decimal import Decimal
from rest_framework.exceptions import ValidationError
from .models import Coupon

class CouponService:
    """
    Handles coupon validation and discount calculation.
    """

    @staticmethod
    def apply_coupon(
        code,
        subtotal,
    ):
        """
        Validate coupon and return
        coupon object + discount amount.
        """

        try:
            coupon = Coupon.objects.get(
                code=code.upper(),
                is_active=True,
            )

        except Coupon.DoesNotExist:

            raise ValidationError(
                "Invalid coupon code."
            )

        if not coupon.is_valid():

            raise ValidationError(
                "Coupon is expired or inactive."
            )

        if subtotal < coupon.minimum_order_amount:

            raise ValidationError(
                f"Minimum order amount should be ₹{coupon.minimum_order_amount}"
            )

        if coupon.discount_type == Coupon.PERCENTAGE:

            discount = (
                subtotal
                * coupon.discount_value
            ) / Decimal("100")

        else:

            discount = coupon.discount_value

        # Discount should never exceed subtotal

        if discount > subtotal:

            discount = subtotal

        return coupon, discount