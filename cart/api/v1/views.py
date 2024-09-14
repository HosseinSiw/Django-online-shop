from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView

from ...models import Cart, CartItem
from store.models import Product
from .serializers import CartSerializer


class MyCartViewEndpoint(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        """Retrieve the cart for the authenticated users."""
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"details": "Not found a cart"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """Update the quantity or details of an item in the cart."""
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"details": "Not found a cart"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serializer = self.serializer_class(cart, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromCartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=id)
        cart = Cart.objects.get(user=user)
        cart_item = get_object_or_404(CartItem, product=product, cart=cart)

        cart_item.delete()

        return Response({
            'message': 'Product removed from cart'
        }, status=status.HTTP_200_OK)


class ClearCartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart.clear()

        return Response({
            'message': 'Cart cleared'
        }, status=status.HTTP_200_OK)
