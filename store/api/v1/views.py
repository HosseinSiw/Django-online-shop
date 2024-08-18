from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from store.models import Product
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
