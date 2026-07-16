from .models import Category, Brand, Product,ProductImage
from .serializers import CategorySerializer,BrandSerializer,ProductSerializer,ProductImageSerializer

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
        "sku",
        "description",
    ]

    ordering_fields = [
        "price",
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