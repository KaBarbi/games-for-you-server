import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import override_settings
from django.core.cache import cache

User = get_user_model()


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.mark.django_db
@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.UserRateThrottle"],
        "DEFAULT_THROTTLE_RATES": {"user": "2/minute"},
    }
)
def test_authenticated_user_throttle_behavior():
    user = User.objects.create_user(
        username="authuser",
        email="authuser@test.com",
        password="StrongPass123",
        full_name="Auth User"
    )

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("game-list")

    response1 = client.get(url)
    response2 = client.get(url)
    assert response1.status_code == 200
    assert response2.status_code == 200

    response3 = client.get(url)
    assert response3.status_code == 429
    assert "throttled" in response3.json()["detail"].lower()
