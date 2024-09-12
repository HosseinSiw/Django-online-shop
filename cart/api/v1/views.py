from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from ...models import Cart, CartItem
from store.models import Product
from .serializers import CartSerializer


class MyCartViewEndpoint(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"details": "Not found a cart"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    Todo: Complete this method.
    def put(self, request, *args, **kwargs):
        # user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    """


class MyCartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        # print(request.user.id)
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return Response({
                'error': 'No cart found for this user.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", ])
def get_cart_by_user_test(request, ):
    print(request.user)
    return Response({"details": "View hit successfully", }, status.HTTP_200_OK)


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
