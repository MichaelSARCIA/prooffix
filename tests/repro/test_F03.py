"""Repro: add_item() silently accepts quantity <= 0, corrupting cart state."""
import pytest
from demo_app.cart import ShoppingCart


def test_add_item_zero_quantity_raises():
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.add_item("X", "Thing", 5.0, 0)


def test_add_item_negative_quantity_raises():
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.add_item("X", "Thing", 5.0, -3)
