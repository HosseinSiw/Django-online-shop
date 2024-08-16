from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer


class UserRegistrationEndPoint(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        """
        Todo: Add email verification
        :param request:
        :return:
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

