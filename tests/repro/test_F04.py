"""Repro: float arithmetic for money — prices must use decimal.Decimal."""
from decimal import Decimal
from demo_app.cart import ShoppingCart, CartItem


def test_cartitem_price_is_decimal():
    """CartItem.price must be stored as Decimal, not float."""
    item = CartItem("X", "Thing", 0.1, 1)
    assert isinstance(item.price, Decimal), (
        f"Expected Decimal, got {type(item.price).__name__}: {item.price!r}"
    )
