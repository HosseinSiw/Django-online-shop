from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from .serializers import CartSerializer
from ...models import Cart


class MyCartViewV2(APIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        serializer = self.serializer_class(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

