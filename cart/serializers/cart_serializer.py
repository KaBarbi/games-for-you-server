from rest_framework import serializers
from cart.models import Cart
from .cart_item_serializer import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "active", "items"]
