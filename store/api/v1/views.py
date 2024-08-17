from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from store.models import Product
from django.shortcuts import get_object_or_404


class ProductHomeView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.filter(is_active=True)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product, slug=slug)
