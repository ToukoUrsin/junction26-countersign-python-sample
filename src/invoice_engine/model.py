from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable
@dataclass(frozen=True)
class TaxRate:
    name: str
    rate: Decimal
    def __post_init__(self):
        if not self.name.strip(): raise ValueError("tax name is required")
        if not Decimal("0") <= self.rate <= Decimal("1"): raise ValueError("tax rate must be 0..1")
@dataclass(frozen=True)
class InvoiceLine:
    description: str
    quantity: Decimal
    unit_price: Decimal
    tax: TaxRate
    discount: Decimal = Decimal("0")
    metadata: dict[str,str] = field(default_factory=dict)
    def __post_init__(self):
        if not self.description.strip(): raise ValueError("description is required")
        if self.quantity <= 0: raise ValueError("quantity must be positive")
        if self.unit_price < 0: raise ValueError("unit price must not be negative")
        if not Decimal("0") <= self.discount <= Decimal("1"): raise ValueError("discount must be 0..1")
    @property
    def net(self): return self.quantity * self.unit_price * (Decimal("1") - self.discount)
@dataclass(frozen=True)
class Invoice:
    number: str
    customer: str
    lines: tuple[InvoiceLine,...]
    currency: str = "EUR"
    notes: str = ""
    def __post_init__(self):
        if not self.number.strip(): raise ValueError("invoice number is required")
        if not self.customer.strip(): raise ValueError("customer is required")
        if not self.lines: raise ValueError("invoice needs at least one line")
        if len(self.currency) != 3 or not self.currency.isalpha(): raise ValueError("currency must be 3 letters")
    @classmethod
    def from_lines(cls, number, customer, lines: Iterable[InvoiceLine], currency="EUR"):
        return cls(number, customer, tuple(lines), currency.upper())
