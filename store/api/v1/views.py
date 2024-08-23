from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .serializers import ProductSerializer, AddToCartSerializer
from .permissions import IsOwnerOrReadOnly
from store.models import Product, CartItem, Cart
from .paginators import CustomProductPaginator


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
    """
    This class handles adding a product to the cart of requested user. Todo: This is an incorrect implementation.
    Tips:
        1. Adding to a cart is an Update operation and nothing else, because we are currently use signals to create
            a cart for each user whenever it registered.
        2. We dont need get and post methods in this endpoint, delete them if there are existed.
    """
    serializer_class = AddToCartSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            product = get_object_or_404(Product, pk=product_id)
            cart = Cart.objects.get(user=user)

            cart_item, created = CartItem.objects.get_or_create(product=product, quantity=quantity, cart=cart)
            cart_item.quantity += quantity
            cart_item.save()

            return Response({
                'message': 'Product added to cart',
                'cart_item_quantity': cart_item.quantity
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)