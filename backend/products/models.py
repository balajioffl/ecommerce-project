from django.db import models
from django.utils.text import slugify
from common.mixins import TimeStampMixin


class Category(TimeStampMixin):
    """
    Product Category
    Example:
        Electronics
        Mobiles
        Laptops
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )


    class Meta:
        db_table = "categories"
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        """
        Automatically generate slug.
        """

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Product Brand
    Example:
        Apple
        Samsung
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "brands"
        ordering = ["name"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampMixin):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
    )

    name = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    short_description = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    is_featured = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    meta_title = models.CharField(
        max_length=255,
        blank=True,
    )

    meta_description = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(TimeStampMixin):
    """
    Stores multiple images for a product.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="products/",
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=1,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "product_images"
        ordering = [
            "display_order",
            "id",
        ]

    def __str__(self):
        return f"{self.product.name} Image"


class Attribute(models.Model):
    """
    Product Attribute

    Examples:
        Color
        Size
        Storage
        RAM
        Material
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "attributes"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """
    Attribute Values

    Examples:

    Color
        Black
        White
        Blue

    Storage
        128GB
        256GB

    Size
        S
        M
        L
    """

    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values",
    )

    value = models.CharField(
        max_length=100,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "attribute_values"

        ordering = [
            "attribute",
            "value",
        ]

        unique_together = (
            "attribute",
            "value",
        )

    def __str__(self):
        return f"{self.attribute.name} : {self.value}"


class ProductVariant(models.Model):
    """
    Sellable variant of a product.

    Example:

    Product : iPhone 16

    Variant 1:
        Black
        128 GB

    Variant 2:
        Black
        256 GB

    Variant 3:
        Blue
        128 GB
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    barcode = models.CharField(
        max_length=100,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "product_variants"

        ordering = [
            "product",
            "sku",
        ]

    def __str__(self):
        return f"{self.product.name} - {self.sku}"


class VariantAttribute(models.Model):
    """
    Connects a Product Variant with its Attribute Values.

    Example:

    Variant:
        iPhone Black 128GB

    Attributes:
        Color   -> Black
        Storage -> 128GB
    """

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="attributes",
    )

    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="variant_attributes",
    )

    class Meta:
        db_table = "variant_attributes"

        ordering = [
            "variant",
        ]

        unique_together = (
            "variant",
            "attribute_value",
        )

    def __str__(self):
        return (
            f"{self.variant.sku} - "
            f"{self.attribute_value.attribute.name}: "
            f"{self.attribute_value.value}"
        )