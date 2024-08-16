from django.utils.translation import gettext_lazy as msg
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ...models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password")

    def create(self, validated_data):
        """
        In this method we create a new user.
        :param validated_data: the data which serializer validate them.
        :return: a new user instance
        """
        validated_data.pop('password1', None)
        return CustomUser.objects.create_user(email=validated_data['email'],password=validated_data['password'],
                                              username=validated_data['username'])

    def validate(self, attrs):
        """
        Password validator method
        :param attrs: attributes of a single request.
        :return: in this case we validate only password and then validate other fields with super() method of base
        (model serializer)
        """
        if not attrs.get('password') == attrs.get('password1'):
            raise serializers.ValidationError({"error": "Passwords don't match", })
        try:
            validate_password(attrs.get("password"))
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"error": msg("User is not verified")})
        validated_data['email'] = self.user.email
        validated_data['username'] = self.user.username
        return validated_data
