from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
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
        serializer.save(cart=cart)
