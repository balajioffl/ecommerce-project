from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from products.models import ProductVariant


class CartService:
    """
    Business logic for Shopping Cart.
    """

    @staticmethod
    def get_cart(user):
        """
        Get or create user's cart.
        """

        cart, _ = Cart.objects.get_or_create(
            user=user,
        )

        return cart

    @staticmethod
    @transaction.atomic
    def add_to_cart(user, variant_id, quantity):
        """
        Add product to cart.
        """

        cart = CartService.get_cart(user)

        variant = get_object_or_404(
            ProductVariant,
            pk=variant_id,
            is_active=True,
        )

        if quantity > variant.stock:
            raise ValueError(
                "Requested quantity exceeds available stock."
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={
                "quantity": quantity,
                "price_at_added": variant.price,
            },
        )

        if not created:

            new_quantity = item.quantity + quantity

            if new_quantity > variant.stock:
                raise ValueError(
                    "Requested quantity exceeds available stock."
                )

            item.quantity = new_quantity

            item.save(
                update_fields=[
                    "quantity",
                ]
            )

        return cart

    @staticmethod
    @transaction.atomic
    def update_quantity(user, item_id, quantity):
        """
        Update quantity.
        """

        cart = CartService.get_cart(user)

        item = get_object_or_404(
            CartItem.objects.select_related(
                "variant",
            ),
            pk=item_id,
            cart=cart,
        )

        if quantity > item.variant.stock:
            raise ValueError(
                "Requested quantity exceeds available stock."
            )

        item.quantity = quantity

        item.save(
            update_fields=[
                "quantity",
            ]
        )

        return cart

    @staticmethod
    @transaction.atomic
    def remove_item(user, item_id):
        """
        Remove one item.
        """

        cart = CartService.get_cart(user)

        item = get_object_or_404(
            CartItem,
            pk=item_id,
            cart=cart,
        )

        item.delete()

        return cart

    @staticmethod
    @transaction.atomic
    def clear_cart(user):
        """
        Remove all items.
        """

        cart = CartService.get_cart(user)

        cart.items.all().delete()

        return cart