from decimal import Decimal
from invoice_engine.rounding import allocate, minor_units, money
def test_allocate_preserves_total():
    parts=allocate(Decimal("10.00"),[Decimal("1"),Decimal("1"),Decimal("1")]); assert sum(parts)==Decimal("10.00"); assert max(parts)-min(parts)<=Decimal("0.01")
def test_currency_minor_units():
    assert minor_units(Decimal("12.34"))==1234; assert minor_units(Decimal("1200"),"JPY")==1200
def test_rounding_modes(): assert money(Decimal("2.345"))==Decimal("2.35")
