"""Repro: grand_total() declared -> float but must return Decimal; body has duplicated branches."""
from decimal import Decimal
from typing import get_type_hints
from demo_app.cart import ShoppingCart


def test_grand_total_annotation_is_decimal():
    """grand_total() return annotation must be Decimal, not float."""
    hints = get_type_hints(ShoppingCart.grand_total)
    assert hints.get("return") is Decimal, (
        f"Expected return annotation Decimal, got {hints.get('return')}"
    )
