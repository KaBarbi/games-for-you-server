from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CartPutSerializer
from .services import CartItemDTO, get_cart_for_user, replace_cart_for_user


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_cart_for_user(user=request.user)
        data = {
            "items": [
                {"productId": item.product_id, "quantity": item.quantity}
                for item in cart.items.all().order_by("id")
            ]
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = CartPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items = [
            CartItemDTO(product_id=i["productId"], quantity=i["quantity"])
            for i in serializer.validated_data["items"]
        ]

        cart = replace_cart_for_user(user=request.user, items=items)

        data = {
            "items": [
                {"productId": item.product_id, "quantity": item.quantity}
                for item in cart.items.all().order_by("id")
            ]
        }
        return Response(data, status=status.HTTP_200_OK)
