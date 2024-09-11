from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .serializers import ProductSerializer, AddToCartSerializer, CartSerializer, CartItemSerializer
from .permissions import IsOwnerOrReadOnly
from store.models import Product, CartItem, Cart
from .paginators import CustomProductPaginator
from users.models import CustomUser as User


class ProductHomeView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.filter(is_active=True)
    pagination_class = CustomProductPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', "name")
    ordering_fields = ('name',)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'slug'

    # queryset = Product.objects.all(), we dont use this type of queryset, instead we use get_queryset method.

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product, slug=slug)


class AddToCartView(APIView):
    serializer_class = AddToCartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id, *args, **kwargs):
        quantity = int(request.data.get('quantity', 1))  # Ensure quantity is an integer
        data = {
            'product_id': id,
            'quantity': quantity,
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = request.user
            product = get_object_or_404(Product, pk=id)

            cart, created = Cart.objects.get_or_create(user=user)

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
                'cart_item_quantity': cart_item.quantity
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyCartView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return Response({
                'error': 'No cart found for this user.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
