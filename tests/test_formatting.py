from decimal import Decimal
from invoice_engine.formatting import format_money
def test_money_symbols():
    assert format_money(Decimal("2.5"),"EUR")=="€2.50"; assert format_money(Decimal("2.5"),"USD")=="$2.50"
