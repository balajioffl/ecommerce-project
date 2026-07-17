from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart Items.
    """

    product_name = serializers.CharField(
        source="variant.product.name",
        read_only=True,
    )

    sku = serializers.CharField(
        source="variant.sku",
        read_only=True,
    )

    unit_price = serializers.DecimalField(
        source="price_at_added",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem

        fields = (
            "id",
            "variant",
            "product_name",
            "sku",
            "quantity",
            "unit_price",
            "subtotal",
        )

    def get_subtotal(self, obj):
        return obj.quantity * obj.price_at_added


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart.
    """

    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart

        fields = (
            "id",
            "user",
            "items",
            "total",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def get_total(self, obj):

        total = 0

        for item in obj.items.all():
            total += item.quantity * item.price_at_added

        return total


class AddToCartSerializer(serializers.Serializer):

    variant = serializers.IntegerField()

    quantity = serializers.IntegerField(
        min_value=1,
    )


class UpdateCartItemSerializer(serializers.Serializer):
    """
    Serializer for updating cart item quantity.
    """

    quantity = serializers.IntegerField(
        min_value=1,
    )