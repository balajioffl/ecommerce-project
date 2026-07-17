from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    Attribute,
    AttributeValue,
    ProductVariant,
    VariantAttribute,
)

from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    ProductImageSerializer,
    AttributeSerializer,
    AttributeValueSerializer,
    ProductVariantSerializer,
    VariantAttributeSerializer,
)

from rest_framework.permissions import AllowAny
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category CRUD operations.
    """

    queryset = Category.objects.all()

    serializer_class = CategorySerializer

    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "is_active",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = [
        "name",
    ]


class BrandViewSet(viewsets.ModelViewSet):

    queryset = Brand.objects.all()

    serializer_class = BrandSerializer

    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["is_active"]

    search_fields = [
        "name",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = [
        "name",
    ]


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Products.
    """

    queryset = Product.objects.select_related(
        "category",
        "brand",
    )

    serializer_class = ProductSerializer

    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "brand",
        "is_active",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "name",
    ]

    ordering = [
        "-created_at",
    ]


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Product Images.
    """

    queryset = ProductImage.objects.select_related(
        "product",
    )

    serializer_class = ProductImageSerializer

    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "product",
        "is_primary",
    ]

    search_fields = [
        "product__name",
        "alt_text",
    ]

    ordering_fields = [
        "display_order",
        "created_at",
    ]

    ordering = [
        "display_order",
    ]


class AttributeViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Product Attributes.
    """

    queryset = Attribute.objects.all()

    serializer_class = AttributeSerializer

    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "is_active",
    ]

    search_fields = [
        "name",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = [
        "name",
    ]


class AttributeValueViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Attribute Values.
    """

    queryset = AttributeValue.objects.select_related(
        "attribute",
    )

    serializer_class = AttributeValueSerializer

    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "attribute",
    ]

    search_fields = [
        "value",
        "attribute__name",
    ]

    ordering_fields = [
        "value",
        "created_at",
    ]

    ordering = [
        "attribute",
        "value",
    ]


class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Product Variants.
    """

    queryset = ProductVariant.objects.select_related(
        "product",
    )

    serializer_class = ProductVariantSerializer

    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "product",
        "is_active",
    ]

    search_fields = [
        "sku",
        "barcode",
        "product__name",
    ]

    ordering_fields = [
        "price",
        "stock",
        "created_at",
    ]

    ordering = [
        "product",
        "sku",
    ]


class VariantAttributeViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Variant Attributes.
    """

    queryset = VariantAttribute.objects.select_related(
        "variant",
        "attribute_value",
        "attribute_value__attribute",
    )

    serializer_class = VariantAttributeSerializer

    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "variant",
    ]

    search_fields = [
        "variant__sku",
        "attribute_value__value",
        "attribute_value__attribute__name",
    ]

    ordering_fields = [
        "variant",
    ]

    ordering = [
        "variant",
    ]