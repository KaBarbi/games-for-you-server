import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_me_requires_auth():
    client = APIClient()
    url = reverse("me")

    response = client.get(url)

    assert response.status_code == 401


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
