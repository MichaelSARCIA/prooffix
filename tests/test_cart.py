"""Passing tests for the shopping cart.

These tests exercise the happy-path and documented behaviour without
accidentally exposing the seeded bugs.
"""

import pytest
from demo_app.cart import ShoppingCart, DISCOUNT_CODES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _single_item_cart() -> ShoppingCart:
    """Cart with exactly one item — avoids the off-by-one in subtotal."""
    cart = ShoppingCart()
    cart.add_item("A001", "Widget", 10.0, 3)
    return cart


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_add_item_creates_entry():
    cart = ShoppingCart()
    cart.add_item("A001", "Widget", 10.0, 1)
    assert cart.item_count() == 1
    assert not cart.is_empty()


def test_add_same_sku_accumulates_quantity():
    cart = ShoppingCart()
    cart.add_item("A001", "Widget", 10.0, 2)
    cart.add_item("A001", "Widget", 10.0, 3)
    # After two adds of the same SKU there should still be one distinct entry
    assert cart.item_count() == 1
    # The combined quantity should be 5
    assert cart._items[0].quantity == 5


def test_remove_item_returns_true_when_present():
    cart = _single_item_cart()
    result = cart.remove_item("A001")
    assert result is True
    assert cart.is_empty()


def test_remove_item_returns_false_when_missing():
    cart = _single_item_cart()
    result = cart.remove_item("DOES_NOT_EXIST")
    assert result is False
    assert cart.item_count() == 1  # original item untouched


def test_update_quantity():
    cart = _single_item_cart()
    updated = cart.update_quantity("A001", 7)
    assert updated is True
    assert cart._items[0].quantity == 7


def test_valid_discount_code_accepted():
    from decimal import Decimal
    cart = _single_item_cart()
    result = cart.apply_discount("SAVE10")
    assert result is True
    assert cart.discount_rate() == Decimal("0.10")


def test_invalid_discount_code_rejected():
    cart = _single_item_cart()
    result = cart.apply_discount("FAKECODE")
    assert result is False
    assert cart.discount_rate() == 0.0


def test_csv_export_contains_headers():
    cart = _single_item_cart()
    csv_output = cart.to_csv()
    assert "SKU" in csv_output
    assert "Grand Total" in csv_output
    assert "A001" in csv_output
