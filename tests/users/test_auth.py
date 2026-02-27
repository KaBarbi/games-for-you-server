import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.core.cache import cache

User = get_user_model()


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


#  REGISTER
@pytest.mark.django_db
@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
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


#  LOGIN
@pytest.mark.django_db
@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
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
        {"email": "kaue@test.com", "password": "StrongPass123"},
        format="json",
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
def test_login_invalid_credentials():
    client = APIClient()
    url = reverse("token_obtain_pair")
    response = client.post(
        url,
        {"email": "wrong@test.com", "password": "wrongpass"},
        format="json",
    )
    assert response.status_code == 401
