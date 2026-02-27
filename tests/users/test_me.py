# tests/users/test_me.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


#  /ME
@pytest.mark.django_db
def test_me_requires_auth():
    client = APIClient()
    url = reverse("me")
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_me_returns_user_data():
    user = User.objects.create_user(
        username="kaue",
        email="kaue@test.com",
        password="StrongPass123",
        full_name="Kaue Barbi",
    )

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("me")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["email"] == user.email
    assert response.data["full_name"] == user.full_name
