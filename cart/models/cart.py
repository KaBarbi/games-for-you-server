from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(active=True),
                name="unique_active_cart_per_user",
            )
        ]

    @property
    def total_price(self):
        """
        Dynamically calculates the sum of all item subtotals in the cart.
        """
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """
        Dynamically calculates the total number of items in the cart.
        """
        return sum(item.quantity for item in self.items.all())
