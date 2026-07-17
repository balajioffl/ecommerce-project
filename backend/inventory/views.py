from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import InventoryTransaction
from .serializers import InventoryTransactionSerializer


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Inventory Transactions.
    """

    queryset = InventoryTransaction.objects.select_related(
        "variant",
        "variant__product",
    )

    serializer_class = InventoryTransactionSerializer

    permission_classes = [
        AllowAny,
    ]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "transaction_type",
        "variant",
    ]

    search_fields = [
        "variant__sku",
        "variant__product__name",
    ]

    ordering_fields = [
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]