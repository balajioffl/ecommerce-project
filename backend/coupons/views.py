from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Coupon
from .serializers import CouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Coupons.
    """

    queryset = Coupon.objects.all()

    serializer_class = CouponSerializer

    permission_classes = [
        AllowAny,
    ]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "discount_type",
        "is_active",
    ]

    search_fields = [
        "code",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "discount_value",
    ]

    ordering = [
        "-created_at",
    ]