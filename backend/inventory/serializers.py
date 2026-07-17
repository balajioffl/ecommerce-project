from rest_framework import serializers

from .models import InventoryTransaction

from django.db import transaction


class InventoryTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Inventory Transactions.
    """

    variant_sku = serializers.CharField(
        source="variant.sku",
        read_only=True,
    )

    product_name = serializers.CharField(
        source="variant.product.name",
        read_only=True,
    )

    class Meta:
        model = InventoryTransaction

        fields = (
            "id",
            "variant",
            "variant_sku",
            "product_name",
            "transaction_type",
            "quantity",
            "note",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
        )


def create(self, validated_data):
    """
    Create inventory transaction and update stock.
    """

    with transaction.atomic():

        variant = validated_data["variant"]

        quantity = validated_data["quantity"]

        inventory = InventoryTransaction.objects.create(
            **validated_data
        )

        variant.stock += quantity

        variant.save(
            update_fields=["stock"]
        )

        return inventory