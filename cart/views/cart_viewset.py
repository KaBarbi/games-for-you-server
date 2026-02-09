from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from cart.serializers import CartSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user, active=True)
