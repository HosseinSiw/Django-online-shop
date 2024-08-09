from ...models import CustomUser
from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ('date_joined', 'last_login')