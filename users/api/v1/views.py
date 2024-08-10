from rest_framework import generics, status
from rest_framework.response import Response
# from mail_templated import EmailMessage

from .serializers import UserRegistrationSerializer


class UserRegisterEndpoint(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            # msg = EmailMessage(template_name="email/activation.tpl", )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
