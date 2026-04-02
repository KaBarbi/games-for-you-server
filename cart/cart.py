from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Cart(user_id={self.user_id})"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items")
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("cart", "product_id")

    def __str__(self) -> str:
        return f"CartItem(cart_id={self.cart_id}, product_id={self.product_id}, qty={self.quantity})"
