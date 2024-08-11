from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from mail_templated import EmailMessage
from rest_framework_simplejwt.views import TokenObtainPairView

from ..utils import EmailThread, get_token_by_user
from .serializers import UserRegistrationSerializer, CustomTokenObtainSerializer, PasswordResetSerializer
from ...models import CustomUser
import jwt


class UserRegisterEndpoint(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            user_obj = CustomUser.objects.get(email=email)
            token = get_token_by_user(user_obj=user_obj)
            data = {
                "email": email,
                "message": "Your account has been created successfully!",
            }
            context = {"user": user_obj, "token": token}
            msg = EmailMessage(template_name="email/activation.tpl", context=context, to=email, )
            EmailThread(msg).start()
            serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainEndpoint(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class UserActivationEndpoint(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, token, *args, **kwargs):
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = token['user_id']
        user_obj = get_object_or_404(CustomUser, pk=user_id)
        if not user_obj.is_verified:
            user_obj.is_verified = True
            user_obj.save()
            return Response({"details": "Your account has been verified",}, status=status.HTTP_200_OK)
        else:
            data = {"details": "Your account is already verified"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetEndPoint(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def put(self, request, username, *args, **kwargs):
        user = get_object_or_404(CustomUser, username=username)

