from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "payment_method",
        "payment_status",
        "amount",
        "paid_at",
    )

    list_filter = (
        "payment_method",
        "payment_status",
    )

    search_fields = (
        "transaction_id",
        "order__order_number",
    )