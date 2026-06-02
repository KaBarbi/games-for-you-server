from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(
            user=self.request.user,
            active=True
        )
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(
            user=self.request.user,
            active=True
        )
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        # Check if the product is already present in the user's active cart
        existing_item = CartItem.objects.filter(
            cart=cart, product=product).first()
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if new_quantity > product.stock:
                raise serializers.ValidationError({
                    "quantity": [
                        f"Cannot add {quantity} more unit(s). Stock limit exceeded (Current in cart: {existing_item.quantity}, Stock: {product.stock})."
                    ]
                })
            existing_item.quantity = new_quantity
            existing_item.save()
            serializer.instance = existing_item
        else:
            serializer.save(cart=cart)
