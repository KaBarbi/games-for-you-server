from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart
from cart.serializers import CartSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user, active=True)

    @action(detail=False, methods=["get", "post"], url_path="current")
    def current(self, request):
        """
        Gets or creates the active shopping cart for the logged-in user.
        """
        cart, _ = Cart.objects.get_or_create(user=request.user, active=True)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="clear")
    def clear(self, request):
        """
        Removes all items from the user's active cart.
        """
        cart, _ = Cart.objects.get_or_create(user=request.user, active=True)
        cart.items.all().delete()
        serializer = self.get_serializer(cart)
        return Response(
            {"message": "Cart cleared successfully.", "cart": serializer.data},
            status=status.HTTP_200_OK
        )

