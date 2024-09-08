from django.conf import settings
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..utils import get_token_for_user
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, PasswordResetSerializer
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


class ForgotPasswordRequestView(APIView):
    def post(self, request, *args, **kwargs):
        """
        In this case we used Email and JWT Token, you can configure your approach appropriately. such as sending sms,
        or other approaches.
        :param request: The main request packet.
        :param args: args
        :param kwargs: kwargs
        :return: It sends A concurrent email and a response with 200 status code.
        """
        user_id = kwargs.get('username')
        user = get_object_or_404(User, username=user_id)
        token = get_token_for_user(user)
        url = request.build_absolute_uri(
            reverse('users:api-urls:reset_password', kwargs={'token': token})
        )
        email_obj = EmailMessage(
            template_name='email/forgot_password.tpl',
            context={"user": user, "url": url},
            to=[user.email],
            from_email="admin@admin.com"
        )
        if user.password_reset_times <= 5:
            user.password_reset_times += 1
            EmailThread(email_obj).start()
            return Response({"msg": "your password reset email sent successfully"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"msg": "your password reset email doesn't sent, you aren't able to reset your password"},
                            status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordConfirmView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, token, *args, **kwargs):
        try:
            # Decode the JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and update the password
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['password_1'])
                user.save()
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
