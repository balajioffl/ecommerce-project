from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
)
from .services import CartService


class CartViewSet(viewsets.ViewSet):
    """
    Shopping Cart APIs
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def list(self, request):
        """
        Get current user's cart.
        """

        cart = CartService.get_cart(
            request.user,
        )

        return Response(
            CartSerializer(cart).data
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="items",
    )
    def add_item(self, request):
        """
        Add item to cart.
        """

        serializer = AddToCartSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        cart = CartService.add_to_cart(
            request.user,
            serializer.validated_data["variant"],
            serializer.validated_data["quantity"],
        )

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="quantity",
    )
    def update_quantity(self, request, pk=None):
        """
        Update cart item quantity.
        """

        serializer = UpdateCartItemSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        cart = CartService.update_quantity(
            request.user,
            pk,
            serializer.validated_data["quantity"],
        )

        return Response(
            CartSerializer(cart).data
        )

    @action(
        detail=True,
        methods=["delete"],
        url_path="remove",
    )
    def remove_item(self, request, pk=None):
        """
        Remove item from cart.
        """

        cart = CartService.remove_item(
            request.user,
            pk,
        )

        return Response(
            CartSerializer(cart).data
        )

    @action(
        detail=False,
        methods=["delete"],
        url_path="clear",
    )
    def clear_cart(self, request):
        """
        Remove all cart items.
        """

        cart = CartService.clear_cart(
            request.user,
        )

        return Response(
            CartSerializer(cart).data
        )