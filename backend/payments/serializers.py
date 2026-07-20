from rest_framework import serializers

from .models import Payment



class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment.
    """

    class Meta:
        model = Payment

        fields = (
            "id",
            "payment_method",
            "payment_status",
            "transaction_id",
            "amount",
            "paid_at",
        )

        read_only_fields = (
            "id",
            "payment_status",
            "transaction_id",
            "amount",
            "paid_at",
        )