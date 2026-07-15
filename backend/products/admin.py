from django.contrib import admin

from .models import Category, Brand, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category.
    """

    list_display = (
        "id",
        "name",
        "slug",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Admin configuration for Brand.
    """

    list_display = (
        "id",
        "name",
        "slug",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = (
        "created_at",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product.
    """

    list_display = (
        "id",
        "name",
        "category",
        "brand",
        "price",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "brand",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "sku",
        "description",
    )

    ordering = (
        "-created_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "category",
        "brand",
    )