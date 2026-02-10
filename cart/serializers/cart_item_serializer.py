from rest_framework import serializers
from cart.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "game",
            "quantity",
        ]
        read_only_fields = ["id"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "A quantidade deve ser maior que zero."
            )
        return value
