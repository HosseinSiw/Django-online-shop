from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .serializers import ProductSerializer, AddToCartSerializer, CartSerializer
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
    """
    Currently It works appropriately, but it needs enhancement (enrichment).
    This class handles adding a product to the cart of the requested user.
    Tips:
        1. Adding to a cart is an Update operation and nothing else, because we are currently using signals to create
            a cart for each user whenever it is registered.
        2. We don't need `get` and `post` methods in this endpoint, delete them if they exist.
    """
    serializer_class = AddToCartSerializer
    permission_classes = (permissions.IsAuthenticated,)  # TODO: Change it to (IsAuthenticated,)

    def post(self, request, id, *args, **kwargs):
        data = {
            'product_id': id,
            'quantity': 1,
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = request.user
            product_id = serializer.validated_data['product_id']


            product = get_object_or_404(Product, pk=product_id)
            cart = Cart.objects.get(user=user)

            # Check if the CartItem already exists; if so, update the quantity.
            cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()

            return Response({
                'message': 'Product added to cart',
                'cart_item_quantity': cart_item.quantity
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyCardView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self, *args, **kwargs):
        user_id = self.request.user.id
        print("User ID: ", user_id)
        user = get_object_or_404(User, id=user_id)
        return get_object_or_404(Cart, user=user)
