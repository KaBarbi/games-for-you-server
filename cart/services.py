from dataclasses import dataclass
from typing import Iterable

from django.db import transaction

from .models import Cart, CartItem


@dataclass(frozen=True)
class CartItemDTO:
    product_id: int
    quantity: int


def _normalize_items(items: Iterable[CartItemDTO]) -> list[CartItemDTO]:
    merged: dict[int, int] = {}
    for it in items:
        merged[it.product_id] = merged.get(it.product_id, 0) + it.quantity

    return [CartItemDTO(product_id=pid, quantity=qty) for pid, qty in merged.items() if qty > 0]


@transaction.atomic
def replace_cart_for_user(*, user, items: list[CartItemDTO]) -> Cart:
    cart, _ = Cart.objects.select_for_update().get_or_create(user=user)

    normalized = _normalize_items(items)

    CartItem.objects.filter(cart=cart).delete()
    CartItem.objects.bulk_create(
        [CartItem(cart=cart, product_id=i.product_id, quantity=i.quantity)
         for i in normalized]
    )

    return cart


def get_cart_for_user(*, user) -> Cart:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart
