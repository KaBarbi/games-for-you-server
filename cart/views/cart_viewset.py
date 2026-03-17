from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Prefetch

from cart.models import Cart, CartItem


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self):
        cart, _ = Cart.objects.get_or_create(
            user=self.request.user,
            active=True
        )
        return cart

    def list(self, request):
        cart = (
            Cart.objects
            .filter(id=self.get_cart().id)
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=CartItem.objects.select_related("product")
                )
            )
            .first()
        )

        from cart.serializers import CartSerializer
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart = self.get_cart()
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response(
                {"error": "Product is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = CartItem.objects.filter(
            cart=cart,
            product_id=product_id
        ).first()

        if item:
            item.quantity += quantity
            item.save()
        else:
            CartItem.objects.create(
                cart=cart,
                product_id=product_id,
                quantity=quantity
            )

        return Response({"message": "Item added"})

    @action(detail=False, methods=["patch"])
    def update_item(self, request):
        cart = self.get_cart()
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity")

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if quantity is not None:
            if int(quantity) <= 0:
                return Response(
                    {"error": "Quantity must be greater than zero"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            item.quantity = int(quantity)
            item.save()

        return Response({"message": "Item updated"})

    @action(detail=False, methods=["delete"])
    def remove_item(self, request):
        cart = self.get_cart()
        item_id = request.data.get("item_id")

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({"message": "Item removed"})
