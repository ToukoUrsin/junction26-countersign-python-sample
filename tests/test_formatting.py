from decimal import Decimal
from invoice_engine import Invoice, InvoiceLine, TaxRate, calculate_totals
from invoice_engine.formatting import format_money, render_summary
from invoice_engine.rounding import minor_units
def test_money_symbols():
    assert format_money(Decimal("2.5"),"EUR")=="€2.50"; assert format_money(Decimal("2.5"),"USD")=="$2.50"
def test_zero_decimal_currencies_print_whole_units():
    assert format_money(Decimal("1200"),"JPY")=="JPY 1200"; assert format_money(Decimal("1200"),"KRW")=="KRW 1200"
def test_zero_decimal_currency_code_is_case_insensitive():
    assert format_money(Decimal("1200"),"jpy")=="JPY 1200"; assert format_money(Decimal("1200"),"Krw")=="KRW 1200"
def test_zero_decimal_amounts_round_half_up_like_minor_units():
    assert format_money(Decimal("1200.5"),"JPY")=="JPY 1201"; assert format_money(Decimal("1200.4"),"JPY")=="JPY 1200"
    assert format_money(Decimal("1200.5"),"KRW")==f"KRW {minor_units(Decimal('1200.5'),'KRW')}"
def test_other_currencies_keep_two_decimals():
    assert format_money(Decimal("2.5"),"GBP")=="£2.50"; assert format_money(Decimal("2.5"),"SEK")=="SEK 2.50"
def test_summary_prints_whole_units_for_zero_decimal_currency():
    yen_line = InvoiceLine("consulting", Decimal("1"), Decimal("1200"), TaxRate("standard", Decimal("0.10")))
    totals = calculate_totals(Invoice.from_lines("I-9","Example",[yen_line],"JPY"))
    assert render_summary(totals).splitlines()==["Subtotal: JPY 1200","Discount: JPY 0","Tax: JPY 120","Total: JPY 1320"]
