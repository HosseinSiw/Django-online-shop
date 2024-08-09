from rest_framework import generics, status
from rest_framework.response import Response


class UserRegister(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        return Response({"details": "ok", status.HTTP_200_OK: request.data})