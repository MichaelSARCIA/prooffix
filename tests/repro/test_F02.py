"""Repro: subtotal() excludes the last item due to range(len-1) off-by-one."""
from demo_app.cart import ShoppingCart


def test_subtotal_includes_all_items():
    cart = ShoppingCart()
    cart.add_item("A", "Widget", 10.0, 1)
    cart.add_item("B", "Gadget", 20.0, 1)
    assert cart.subtotal() == 30.0, f"Expected 30.0, got {cart.subtotal()}"


def test_subtotal_single_item_not_zero():
    cart = ShoppingCart()
    cart.add_item("A", "Widget", 10.0, 2)
    assert cart.subtotal() == 20.0, f"Expected 20.0, got {cart.subtotal()}"
