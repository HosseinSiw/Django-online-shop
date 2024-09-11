from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.api.v1.serializers import OrderSerializer
from orders.models import Order
from store.models import Cart


class OrderListAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        orders = Order.objects.filter(cart=cart)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)
