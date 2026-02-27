import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings
    from copy import deepcopy

    default_db = deepcopy(settings.DATABASES["default"])

    default_db.update({
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    })

    settings.DATABASES["default"] = default_db


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
