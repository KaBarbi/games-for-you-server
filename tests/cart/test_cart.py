import pytest
from django.urls import reverse
from cart.models import Cart, CartItem
from games.models import Game


@pytest.mark.django_db
def test_get_current_cart_unauthenticated(api_client):
    """
    Ensure that unauthenticated users cannot retrieve the current cart.
    """
    url = reverse("cart-current")
    response = api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_current_cart_creates_cart_if_not_exists(auth_client, user):
    """
    Ensure that retrieving the current cart automatically creates a new active
    cart for the user if one does not already exist.
    """
    assert Cart.objects.filter(user=user, active=True).count() == 0

    url = reverse("cart-current")
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data["active"] is True
    assert len(response.data["items"]) == 0
    assert float(response.data["total_price"]) == 0.00
    assert response.data["total_items"] == 0
    assert Cart.objects.filter(user=user, active=True).count() == 1


@pytest.mark.django_db
def test_get_current_cart_returns_existing_cart(auth_client, user):
    """
    Ensure that retrieving the current cart returns the user's existing
    active cart instead of creating a new one.
    """
    existing_cart = Cart.objects.create(user=user, active=True)

    url = reverse("cart-current")
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == existing_cart.id
    assert Cart.objects.filter(user=user, active=True).count() == 1


@pytest.mark.django_db
def test_clear_cart(auth_client, user):
    """
    Ensure that the clear action removes all items from the current user's active cart.
    """
    cart = Cart.objects.create(user=user, active=True)
    game = Game.objects.create(
        title="Test Game",
        price=59.99,
        stock=5,
        platform="PS"
    )
    CartItem.objects.create(cart=cart, product=game, quantity=2)

    assert cart.items.count() == 1
    assert cart.total_items == 2
    assert float(cart.total_price) == 119.98

    url = reverse("cart-clear")
    response = auth_client.post(url)

    assert response.status_code == 200
    assert response.data["message"] == "Cart cleared successfully."
    assert len(response.data["cart"]["items"]) == 0
    assert float(response.data["cart"]["total_price"]) == 0.00
    assert response.data["cart"]["total_items"] == 0
    assert cart.items.count() == 0
