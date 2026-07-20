from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem, ShippingAddress
from uuid import uuid4
from payments.services import PaymentService


class CheckoutService:

    # uuid generator

    @staticmethod
    def generate_order_number():

        return f"ORD-{uuid4().hex[:10].upper()}"

    # checkout

    @staticmethod
    @transaction.atomic
    def checkout(user, shipping_data):
        """
        Convert Cart into Order.
        """

        cart = Cart.objects.prefetch_related("items__variant").get(user=user)

        # validate cart

        if not cart.items.exists():
            raise ValueError("Your cart is empty.")

        # validate stock

        for item in cart.items.all():

            if item.quantity > item.variant.stock:

                raise ValueError(f"Insufficient stock for {item.variant.sku}")

        subtotal = 0

        for item in cart.items.all():
            subtotal += item.quantity * item.price_at_added

        # create order

        order = Order.objects.create(
            user=user,
            order_number=CheckoutService.generate_order_number(),
            subtotal=subtotal,
            tax_amount=0,
            shipping_charge=0,
            discount_amount=0,
            total_amount=subtotal,
        )

        for item in cart.items.select_related("variant"):

            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                product_name=item.variant.product.name,
                sku=item.variant.sku,
                unit_price=item.price_at_added,
                quantity=item.quantity,
                total_price=(item.quantity * item.price_at_added),
            )

        ShippingAddress.objects.create(
            order=order,
            full_name=shipping_data["full_name"],
            phone_number=shipping_data["phone_number"],
            address_line_1=shipping_data["address_line_1"],
            address_line_2=shipping_data.get(
                "address_line_2",
                "",
            ),
            city=shipping_data["city"],
            state=shipping_data["state"],
            postal_code=shipping_data["postal_code"],
            country=shipping_data.get(
                "country",
                "India",
            ),
        )
        
        PaymentService.create_payment(
            order=order,
            payment_method=shipping_data[
                "payment_method"
                ],
        )


        for item in cart.items.select_related("variant"):

            variant = item.variant

            variant.stock -= item.quantity

            variant.save(
                update_fields=[
                    "stock",
                ]
            )

        cart.items.all().delete()

        return order