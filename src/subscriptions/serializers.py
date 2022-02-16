from rest_framework import serializers


class CreateCheckoutSerializer(serializers.Serializer):
    price_id = serializers.CharField(max_length=50)
