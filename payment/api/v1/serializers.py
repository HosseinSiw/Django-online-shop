from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(max_length=255)
