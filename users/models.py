from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True)
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
