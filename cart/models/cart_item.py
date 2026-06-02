from django.db import models
from .cart import Cart


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items",
                             on_delete=models.CASCADE)
    product = models.ForeignKey("games.Game", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        """
        Returns the subtotal for this item (quantity * product price).
        """
        return self.product.price * self.quantity

