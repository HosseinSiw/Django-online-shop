from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.utils.translation import gettext_lazy as _
from ...models import CustomUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password")
        read_only_fields = ('date_joined', 'last_login')

    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password'):
            raise serializers.ValidationError("Passwords doesn't match")

        try:
            validate_password(attrs.get('password1'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1')
        username, password, email = validated_data.get("username"), validated_data.get("password"), validated_data.get(
            "email")
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        return user


class CustomTokenObtainSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError(_("User isn't verified"))
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True, required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = attrs.get('email')
        user = CustomUser.objects.get(email=email)
        if user is not None:
            return validated_data
        else:
            return serializers.ValidationError(_("Email doesn't exist"))


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

