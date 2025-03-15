from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions

from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import ProductSerializerV2
from ...models import Product
from .paginators import CustomProductPaginatorV2


class ProductListAPIViewV2(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerV2
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomProductPaginatorV2
    search_fields = ['name',]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    ordering_fields = ('name',)


class ProductDetailAPIViewV2(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerV2
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        slug = self.kwargs['slug']
        return get_object_or_404(Product.objects.all(), slug=slug,)
