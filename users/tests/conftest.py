import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@test.com",
        password="123456",
        full_name="Test User"
    )


@pytest.fixture
def auth_client(api_client, user):
    response = api_client.post(
        "/api/users/login/",
        {
            "email": user.email,
            "password": "123456",
        },
        format="json",
    )

    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client
