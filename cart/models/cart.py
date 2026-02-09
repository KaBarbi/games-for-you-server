from django.db import models
from django.conf import settings
from users.serializers.user_serializers import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(active=True),
                name="unique_active_cart_per_user",
            )
        ]
