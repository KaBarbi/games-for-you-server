import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    url = reverse("register")

    payload = {
        "username": "kaue",
        "email": "kaue@test.com",
        "password": "StrongPass123",
        "password2": "StrongPass123",
    }

    response = client.post(url, payload, format="json")

    assert response.status_code == 201
    assert response.data["email"] == "kaue@test.com"


@pytest.mark.django_db
def test_login_returns_jwt():
    user = User.objects.create_user(
        username="kaue",
        email="kaue@test.com",
        password="StrongPass123",
    )

    client = APIClient()
    url = reverse("token_obtain_pair")

    response = client.post(
        url,
        {
            "email": "kaue@test.com",
            "password": "StrongPass123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_invalid_credentials():
    client = APIClient()
    url = reverse("token_obtain_pair")

    response = client.post(
        url,
        {
            "email": "wrong@test.com",
            "password": "wrongpass",
        },
        format="json",
    )

    assert response.status_code == 401
