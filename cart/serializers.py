from rest_framework import serializers


class CartItemInputSerializer(serializers.Serializer):
    productId = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, max_value=999)


class CartPutSerializer(serializers.Serializer):
    items = CartItemInputSerializer(many=True)


class CartItemOutputSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, max_value=999)


class CartOutputSerializer(serializers.Serializer):
    items = CartItemOutputSerializer(many=True)
