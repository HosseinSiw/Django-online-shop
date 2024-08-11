from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from mail_templated import EmailMessage
from rest_framework_simplejwt.views import TokenObtainPairView

from ..utils import EmailThread, get_token_by_user
from .serializers import (UserRegistrationSerializer,
                          CustomTokenObtainSerializer,
                          PasswordResetSerializer,
                          ResetPasswordRequestSerializer)
from ...models import CustomUser, PasswordResetModel
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
            return Response({"details": "Your account has been verified"}, status=status.HTTP_200_OK)
        else:
            data = {"details": "Your account is already verified"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResettingEndpoint(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        email = serializer['email']
        user = CustomUser.objects.filter(email__iexact=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordResetModel(email=email, token=token, user=user)
            if reset.time_valid():
                reset.save()
                context = {
                    "user": user, "token": token,
                }
                email_obj = EmailMessage(template_name="email/password_reset.tpl", context=context,to=email,)
                EmailThread(email_obj).start()
                return Response({"details": "We have sent you a link, check it and reset your password"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"details": "You aren't able to reset your password"},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({"details": "BAD REQUEST"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetEndpoint(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordResetSerializer

    def post(self, request, token, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password != confirm_password:
            return Response({"details": "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

        reset_obj = PasswordResetModel(token=token,)
        if not reset_obj.time_valid() and reset_obj is not None:
            return Response({"token": "Token expired."})

        user = CustomUser.objects.filter(email=reset_obj.user.email).first()
        if user:
            user.set_password(new_password)
            user.save()
            reset_obj.verified = False
            return Response({"details": "Your new password has been set."}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "Provided email doesn't exists."}, status=status.HTTP_400_BAD_REQUEST)
