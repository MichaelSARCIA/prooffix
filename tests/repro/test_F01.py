"""Repro: eval() on user-supplied discount code enables arbitrary code execution."""
import os
import pytest
from demo_app.cart import ShoppingCart


def test_apply_discount_does_not_execute_injected_code():
    cart = ShoppingCart()
    cart.add_item("A", "Widget", 10.0, 1)
    # Craft a payload that sets an env var if eval() runs the injected expression
    payload = "SAVE10') ; os.environ.__setitem__('PWNED','yes') ; ('"
    cart.apply_discount(payload)
    assert os.environ.get("PWNED") is None, "eval() executed injected code — RCE confirmed"
