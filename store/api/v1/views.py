from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import ProductSerializer
from store.models import Product


class ProductHomeView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    queryset = Product.objects.filter(is_active=True)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    pass
