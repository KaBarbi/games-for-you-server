import pytest
from django.urls import reverse
from cart.models import Cart, CartItem
from games.models import Game


@pytest.fixture
def game():
    return Game.objects.create(
        title="Epic Adventure",
        price=49.99,
        stock=5,
        platform="PS"
    )


@pytest.mark.django_db
def test_add_item_to_cart(auth_client, user, game):
    """
    Ensure that we can successfully add a valid game to our cart.
    """
    url = reverse("cartitem-list")
    data = {
        "product": game.id,
        "quantity": 2
    }
    response = auth_client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["product"] == game.id
    assert response.data["quantity"] == 2
    assert float(response.data["subtotal"]) == 99.98
    assert response.data["product_details"]["title"] == "Epic Adventure"


@pytest.mark.django_db
def test_add_item_stock_limit_exceeded(auth_client, user, game):
    """
    Ensure that we cannot add a quantity that exceeds the game's available stock.
    """
    url = reverse("cartitem-list")
    data = {
        "product": game.id,
        "quantity": 6  # game.stock is 5
    }
    response = auth_client.post(url, data, format="json")

    assert response.status_code == 400
    assert "quantity" in response.data
    assert "in stock" in response.data["quantity"][0].lower()


@pytest.mark.django_db
def test_add_item_invalid_quantity(auth_client, user, game):
    """
    Ensure that we cannot add items with negative or zero quantities.
    """
    url = reverse("cartitem-list")
    
    # Test zero quantity
    response = auth_client.post(url, {"product": game.id, "quantity": 0}, format="json")
    assert response.status_code == 400
    assert "quantity" in response.data

    # Test negative quantity
    response = auth_client.post(url, {"product": game.id, "quantity": -3}, format="json")
    assert response.status_code == 400
    assert "quantity" in response.data


@pytest.mark.django_db
def test_add_duplicate_item_merges_quantity(auth_client, user, game):
    """
    Ensure that adding the same item multiple times merges the quantity
    into a single CartItem instead of creating a duplicate row.
    """
    url = reverse("cartitem-list")

    # Add first time
    response1 = auth_client.post(url, {"product": game.id, "quantity": 2}, format="json")
    assert response1.status_code == 201

    # Add second time
    response2 = auth_client.post(url, {"product": game.id, "quantity": 2}, format="json")
    assert response2.status_code == 201
    
    # We should have exactly 1 cart item with quantity = 4
    cart = Cart.objects.get(user=user, active=True)
    assert cart.items.count() == 1
    
    item = cart.items.first()
    assert item.quantity == 4
    assert float(item.subtotal) == 199.96
    
    # Response should also return the updated merged item
    assert response2.data["id"] == item.id
    assert response2.data["quantity"] == 4


@pytest.mark.django_db
def test_add_duplicate_item_exceeds_stock_on_merge(auth_client, user, game):
    """
    Ensure that merging duplicate item quantities validates cumulative stock correctly.
    """
    url = reverse("cartitem-list")

    # Add first time (quantity 3)
    response1 = auth_client.post(url, {"product": game.id, "quantity": 3}, format="json")
    assert response1.status_code == 201

    # Add second time (quantity 3, total 6, stock is 5)
    response2 = auth_client.post(url, {"product": game.id, "quantity": 3}, format="json")
    assert response2.status_code == 400
    assert "quantity" in response2.data
    assert "stock limit exceeded" in response2.data["quantity"][0].lower()


@pytest.mark.django_db
def test_update_item_quantity(auth_client, user, game):
    """
    Ensure that we can update the quantity of a cart item.
    """
    cart = Cart.objects.create(user=user, active=True)
    item = CartItem.objects.create(cart=cart, product=game, quantity=2)

    url = reverse("cartitem-detail", kwargs={"pk": item.id})
    response = auth_client.patch(url, {"quantity": 4}, format="json")

    assert response.status_code == 200
    assert response.data["quantity"] == 4
    assert float(response.data["subtotal"]) == 199.96


@pytest.mark.django_db
def test_update_item_quantity_exceeds_stock(auth_client, user, game):
    """
    Ensure that updating a cart item to a quantity that exceeds stock is validated and rejected.
    """
    cart = Cart.objects.create(user=user, active=True)
    item = CartItem.objects.create(cart=cart, product=game, quantity=2)

    url = reverse("cartitem-detail", kwargs={"pk": item.id})
    response = auth_client.patch(url, {"quantity": 6}, format="json")  # stock is 5

    assert response.status_code == 400
    assert "quantity" in response.data


@pytest.mark.django_db
def test_delete_item_from_cart(auth_client, user, game):
    """
    Ensure that we can delete an item from the cart.
    """
    cart = Cart.objects.create(user=user, active=True)
    item = CartItem.objects.create(cart=cart, product=game, quantity=2)

    assert cart.items.count() == 1

    url = reverse("cartitem-detail", kwargs={"pk": item.id})
    response = auth_client.delete(url)

    assert response.status_code == 204
    assert cart.items.count() == 0
