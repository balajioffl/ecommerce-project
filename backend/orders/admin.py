from django.contrib import admin

from .models import (
    Order,
    OrderItem,
    ShippingAddress,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product_name",
        "sku",
        "unit_price",
        "quantity",
        "total_price",
    )


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "user",
        "status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "user__email",
    )

    inlines = [
        ShippingAddressInline,
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product_name",
        "sku",
        "quantity",
        "unit_price",
        "total_price",
    )


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "full_name",
        "city",
        "state",
        "country",
    )