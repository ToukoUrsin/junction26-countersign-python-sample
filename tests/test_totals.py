from decimal import Decimal
import pytest
from invoice_engine import Invoice, InvoiceLine, TaxRate, calculate_totals
VAT = TaxRate("standard", Decimal("0.24"))
def line(price="100", qty="1", discount="0"): return InvoiceLine("consulting", Decimal(qty), Decimal(price), VAT, Decimal(discount))
def test_totals_round_each_line_and_total():
    result = calculate_totals(Invoice.from_lines("I-1","Example",[line("10.005"),line("10.005")]))
    assert result.subtotal == Decimal("20.01"); assert result.tax == Decimal("4.80"); assert result.total == Decimal("24.81")
def test_welcome_discount_applies():
    result = calculate_totals(Invoice.from_lines("I-2","Example",[line("100")]), "welcome")
    assert result.discount == Decimal("5.00"); assert result.total == Decimal("117.80")
def test_partner_minimum_is_inclusive():
    result = calculate_totals(Invoice.from_lines("I-3","Example",[line("1000")]), "PARTNER")
    assert result.discount == Decimal("100.00")
def test_validation():
    with pytest.raises(ValueError): InvoiceLine("",Decimal("1"),Decimal("1"),VAT)
    with pytest.raises(ValueError): InvoiceLine("x",Decimal("0"),Decimal("1"),VAT)

def test_invoice_rebate_code_is_used_when_no_override():
    invoice = Invoice.from_lines("I-4", "Example", [line("100")], rebate_code="WELCOME")
    result = calculate_totals(invoice)
    assert result.discount == Decimal("5.00")

def test_explicit_code_overrides_invoice_code():
    invoice = Invoice.from_lines("I-5", "Example", [line("100")], rebate_code="WELCOME")
    result = calculate_totals(invoice, "NONPROFIT")
    assert result.discount == Decimal("0.00")

def test_blank_rebate_code_is_rejected():
    with pytest.raises(ValueError): Invoice.from_lines("I-6", "Example", [line("100")], rebate_code=" ")
