from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order
from .serializers import (
    OrderSerializer,
    CheckoutSerializer,
)
from .services import CheckoutService

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Order APIs.
    """

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user,
        ).prefetch_related(
            "items",
        ).select_related(
            "shipping_address",
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="checkout",
    )
    def checkout(self, request):
        """
        Convert Cart into Order.
        """

        serializer = CheckoutSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        order = CheckoutService.checkout(
            user=request.user,
            shipping_data=serializer.validated_data,
        )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )