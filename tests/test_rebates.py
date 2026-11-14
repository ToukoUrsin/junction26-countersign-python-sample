from decimal import Decimal
import pytest
from invoice_engine import Invoice, InvoiceLine, TaxRate, calculate_totals
VAT = TaxRate("standard", Decimal("0.24"))

def make_invoice(amount, code=None):
    line = InvoiceLine("advisory", Decimal("1"), Decimal(str(amount)), VAT)
    return Invoice.from_lines("REB-1", "Sample Client", [line], rebate_code=code)

def test_codes_are_case_insensitive():
    assert calculate_totals(make_invoice("100"), "wElCoMe").discount == Decimal("5.00")

def test_unknown_code_is_ignored():
    result = calculate_totals(make_invoice("100"), "SPRING")
    assert result.discount == Decimal("0.00")

def test_welcome_has_no_minimum():
    assert calculate_totals(make_invoice("0.01"), "WELCOME").discount == Decimal("0.00")

def test_partner_above_minimum():
    assert calculate_totals(make_invoice("1000.01"), "PARTNER").discount == Decimal("100.00")

def test_nonprofit_above_minimum():
    assert calculate_totals(make_invoice("500.01"), "NONPROFIT").discount == Decimal("75.00")

def test_invoice_code_is_used_for_nonprofit():
    assert calculate_totals(make_invoice("500.01", "NONPROFIT")).discount == Decimal("75.00")

def test_explicit_empty_string_is_an_override():
    invoice = make_invoice("100", "WELCOME")
    assert calculate_totals(invoice, "").discount == Decimal("0.00")

def test_rebate_is_reflected_in_taxable_amount():
    result = calculate_totals(make_invoice("100", "WELCOME"))
    assert result.taxable == Decimal("95.00")
    assert result.tax == Decimal("22.80")
    assert result.total == Decimal("117.80")

def test_invoice_rebate_code_is_optional():
    invoice = make_invoice("100")
    assert invoice.rebate_code is None
    assert calculate_totals(invoice).discount == Decimal("0.00")

def test_rebate_code_is_preserved_on_invoice():
    assert make_invoice("100", "WELCOME").rebate_code == "WELCOME"

def test_invalid_rebate_codes_fail_early():
    with pytest.raises(ValueError, match="blank"):
        make_invoice("100", " ")

def test_existing_customer_and_number_are_unchanged():
    invoice = make_invoice("100", "WELCOME")
    assert invoice.customer == "Sample Client"
    assert invoice.number == "REB-1"
