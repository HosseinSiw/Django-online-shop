from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..utils import get_token_for_user
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from ...models import CustomUser as User
from ..utils import EmailThread
import jwt


class UserRegistrationEndPoint(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        """
        :param request: the main request packet.
        :return: a not verified user instance.
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            user_obj = get_object_or_404(User, email=email)
            token = get_token_for_user(user=user_obj)
            email_obj = EmailMessage('email/active.tpl',
                                     {"token": token, "user": user_obj},
                                     "admin1@admin.com",
                                     to=[email])
            EmailThread(email_obj).start()
            data = {
                "email": email,
                "msg": "your account created successfully check your inbox and verify your account",
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    I create my own endpoint to modify the base serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserVerificationEndPoint(APIView):
    def get(self, request, token, *args, **kwargs):
        user_id = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])['user_id']
        user = User.objects.get(pk=user_id)  # or get_object_or_404(User, id=id)
        if user is not None and not user.is_verified:
            user.is_verified = True
            user.save()
            return Response({"msg": "your account has been verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "your account isn't registered, register first."},
                            status=status.HTTP_400_BAD_REQUEST)
