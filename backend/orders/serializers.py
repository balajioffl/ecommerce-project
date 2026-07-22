from rest_framework import serializers

from .models import (
    Order,
    OrderItem,
    ShippingAddress,
)

from payments.serializers import PaymentSerializer


class ShippingAddressSerializer(serializers.ModelSerializer):
    """
    Serializer for Shipping Address.
    """

    class Meta:
        model = ShippingAddress

        fields = (
            "full_name",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
        )


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Order Items.
    """

    class Meta:
        model = OrderItem

        fields = (
            "id",
            "product_name",
            "sku",
            "unit_price",
            "quantity",
            "total_price",
        )


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Orders.
    """

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    shipping_address = ShippingAddressSerializer(
        read_only=True,
    )

    payment = PaymentSerializer(
        read_only=True,
    )

    class Meta:
        model = Order

        fields = (
            "id",
            "order_number",
            "status",
            "subtotal",
            "tax_amount",
            "shipping_charge",
            "discount_amount",
            "total_amount",
            "created_at",
            "items",
            "shipping_address",
            "payment",
        )


class CheckoutSerializer(serializers.Serializer):
    """
    Serializer for Checkout Request.
    """

    full_name = serializers.CharField(
        max_length=255,
    )

    phone_number = serializers.CharField(
        max_length=20,
    )

    address_line_1 = serializers.CharField(
        max_length=255,
    )

    address_line_2 = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )

    city = serializers.CharField(
        max_length=100,
    )

    state = serializers.CharField(
        max_length=100,
    )

    postal_code = serializers.CharField(
        max_length=20,
    )

    country = serializers.CharField(
        max_length=100,
        required=False,
        default="India",
    )

    payment_method = serializers.ChoiceField(
        choices=[
            "COD",
            "RAZORPAY",
            "STRIPE",
        ]
    )

    coupon_code = serializers.CharField(
        required=False,
        allow_blank=True,
    )
