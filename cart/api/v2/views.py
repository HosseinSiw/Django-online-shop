from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import CartSerializer, AddToCartSerializer
from ...models import Cart, CartItem
from store.models import Product as ProductModel


class MyCartViewV2(APIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        user = request.user
        try:
            cart = Cart.objects.prefetch_related('items').get(user=user)
            print("Cart is correct\n\n\n\n\n\n\n")
            serializer = CartSerializer(instance=cart,)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddToCartViewV2(APIView):
    serializer_class = AddToCartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, product_id, *args, **kwargs):
        quantity = int(request.data.get('quantity', 1))  # Ensure quantity is an integer
        data = {
            'product_id': id,
            'quantity': quantity,
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = request.user  # Because this endpoint is for authenticated users.
            product = get_object_or_404(ProductModel, pk=product_id)

            cart = Cart.objects.get(user=user)

            # Check if the CartItem already exists; if so, update the quantity.
            cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
            cart_item.quantity += quantity

            # Validate if the quantity does not exceed available stock
            if cart_item.quantity > product.stock:
                return Response({
                    'error': 'Quantity exceeds available stock.'
                }, status=status.HTTP_400_BAD_REQUEST)

            cart_item.save()

            return Response({
                'message': 'Product added to cart',
                'cart_item_quantity': cart_item.quantity,
                "product name": product.name,
                "product owner": product.owner.username,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartClearViewV2(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
      user = request.user
      cart = Cart.objects.get(user=user)
      cart.clear_cart()
      return Response(data={"Message": "Cart has been cleared"},
                      status=status.HTTP_200_OK)
