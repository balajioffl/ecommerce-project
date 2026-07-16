import os
from rest_framework import serializers

from .models import Category, Brand, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product.
    """

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    brand_name = serializers.CharField(
        source="brand.name",
        read_only=True,
    )

    class Meta:
        model = Product

        fields = (
            "id",
            "category",
            "category_name",
            "brand",
            "brand_name",
            "name",
            "slug",
            "sku",
            "description",
            "price",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "slug",
            "created_at",
            "updated_at",
        )


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for Product Images.
    """

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = ProductImage

        fields = (
            "id",
            "product",
            "product_name",
            "image",
            "alt_text",
            "display_order",
            "is_primary",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_image(self, image):
        """
        Validate uploaded image.
        """

        allowed_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        )

        extension = os.path.splitext(
            image.name
        )[1].lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )

        max_size = 5 * 1024 * 1024  # 5 MB

        if image.size > max_size:
            raise serializers.ValidationError(
                "Image size must be less than 5 MB."
            )

        return image

    def create(self, validated_data):
        """
        If this image is marked as primary,
        remove the primary flag from all other
        images of the same product.
        """

        if validated_data.get("is_primary"):

            ProductImage.objects.filter(
                product=validated_data["product"],
                is_primary=True,
            ).update(
                is_primary=False
            )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        If image becomes primary,
        unset previous primary image.
        """

        is_primary = validated_data.get(
            "is_primary",
            instance.is_primary,
        )

        product = validated_data.get(
            "product",
            instance.product,
        )

        if is_primary:

            ProductImage.objects.filter(
                product=product,
                is_primary=True,
            ).exclude(
                pk=instance.pk,
            ).update(
                is_primary=False
            )

        return super().update(
            instance,
            validated_data,
        )