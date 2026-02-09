from django.db import models
from .cart import Cart


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items",
                             on_delete=models.CASCADE)
    product = models.ForeignKey("games.Game", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
