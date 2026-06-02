from rest_framework import serializers
from cart.models import CartItem
from games.serializers import GameSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_details = GameSerializer(source="product", read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_details', 'quantity', 'subtotal']
        read_only_fields = ["id"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        return value

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")

        # If it is an update, instance exists and we fallback to existing values if not provided
        if self.instance:
            product = product or self.instance.product
            quantity = quantity if quantity is not None else self.instance.quantity

        if product and quantity > product.stock:
            raise serializers.ValidationError({
                "quantity": f"Only {product.stock} unit(s) of '{product.title}' are available in stock."
            })
        return attrs

