from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...models import CustomUser
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password")

    def create(self, validated_data):
        validated_data.pop('password1', None)
        return CustomUser.objects.create_user(email=validated_data['email'],password=validated_data['password'],
                                              username=validated_data['username'])

    def validate(self, attrs):
        if not attrs.get('password') == attrs.get('password1'):
            raise serializers.ValidationError({"error": "Passwords don't match", })
        try:
            validate_password(attrs.get("password"))
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)
