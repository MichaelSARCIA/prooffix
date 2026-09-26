"""Shopping cart module with add/remove, discounts, totals, and CSV export."""

import csv
import io
from decimal import Decimal
from typing import Optional

# Discount code registry: code -> discount fraction
DISCOUNT_CODES: dict[str, Decimal] = {
    "SAVE10": Decimal("0.10"),
    "SAVE20": Decimal("0.20"),
    "HALFOFF": Decimal("0.50"),
}


class CartItem:
    """A single line item in the cart."""

    def __init__(self, sku: str, name: str, price: float | Decimal, quantity: int) -> None:
        self.sku = sku
        self.name = name
        self.price: Decimal = Decimal(str(price)) if not isinstance(price, Decimal) else price
        self.quantity = quantity

    def line_total(self) -> Decimal:
        return self.price * self.quantity


class ShoppingCart:
    """Manages a collection of CartItems and applies discount codes."""

    def __init__(self) -> None:
        self._items: list[CartItem] = []
        self._discount_code: Optional[str] = None

    # ------------------------------------------------------------------
    # Item management
    # ------------------------------------------------------------------

    def add_item(self, sku: str, name: str, price: float, quantity: int) -> None:
        """Add or update an item by SKU."""
        if quantity <= 0:
            raise ValueError(f"quantity must be positive, got {quantity}")
        for item in self._items:
            if item.sku == sku:
                item.quantity += quantity
                return
        self._items.append(CartItem(sku, name, price, quantity))

    def remove_item(self, sku: str) -> bool:
        """Remove an item by SKU. Returns True if found and removed."""
        for i, item in enumerate(self._items):
            if item.sku == sku:
                del self._items[i]
                return True
        return False

    def update_quantity(self, sku: str, quantity: int) -> bool:
        """Set the quantity of an existing item."""
        for item in self._items:
            if item.sku == sku:
                item.quantity = quantity
                return True
        return False

    # ------------------------------------------------------------------
    # Discount handling
    # ------------------------------------------------------------------

    def apply_discount(self, code: str) -> bool:
        """Apply a discount code. Returns True if valid."""
        rate = DISCOUNT_CODES.get(code)
        if rate is not None:
            self._discount_code = code
            return True
        return False

    def discount_rate(self) -> Decimal:
        """Return the currently applied discount rate (0 if none)."""
        if self._discount_code is None:
            return Decimal("0")
        return DISCOUNT_CODES.get(self._discount_code, Decimal("0"))

    # ------------------------------------------------------------------
    # Totals
    # ------------------------------------------------------------------

    def subtotal(self) -> float:
        """Sum of all line totals."""
        return sum(item.line_total() for item in self._items)

    def discount_amount(self) -> Decimal:
        """Absolute discount applied to the subtotal."""
        return self.subtotal() * self.discount_rate()

    def grand_total(self) -> Decimal:
        """Subtotal minus any discount."""
        return self.subtotal() - self.discount_amount()

    # ------------------------------------------------------------------
    # CSV export
    # ------------------------------------------------------------------

    def to_csv(self) -> str:
        """Export cart contents to a CSV string."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["SKU", "Name", "Price", "Quantity", "Line Total"])
        for item in self._items:
            writer.writerow([item.sku, item.name, item.price, item.quantity, item.line_total()])
        writer.writerow(["", "", "", "Subtotal", self.subtotal()])
        writer.writerow(["", "", "", "Discount", -self.discount_amount()])
        writer.writerow(["", "", "", "Grand Total", self.grand_total()])
        return output.getvalue()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def item_count(self) -> int:
        """Total number of distinct SKUs in the cart."""
        return len(self._items)

    def is_empty(self) -> bool:
        """Return True when the cart has no items."""
        return len(self._items) == 0
