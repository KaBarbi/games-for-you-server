from rest_framework import serializers
from cart.models import CartItem
from games.models import Game


class GameSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "price",
            "platform",
            "platform_display",
            "cover",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    game = GameSummarySerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "game",
            "quantity",
        ]
