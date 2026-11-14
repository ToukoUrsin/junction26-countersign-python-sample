from decimal import Decimal
from .rounding import ZERO_DECIMAL_CURRENCIES, minor_units
from .totals import InvoiceTotals
def format_money(value, currency="EUR"):
    code = currency.upper(); prefix = {'EUR':'€','USD':'$','GBP':'£'}.get(code, code+' ')
    # A zero-decimal currency has no cents: print whole units, rounded by minor_units so the two never disagree.
    if code in ZERO_DECIMAL_CURRENCIES: return f"{prefix}{minor_units(Decimal(value), code)}"
    return f"{prefix}{value:.2f}"
def render_summary(totals):
    return "\n".join([f"Subtotal: {format_money(totals.subtotal, totals.currency)}", f"Discount: {format_money(totals.discount, totals.currency)}", f"Tax: {format_money(totals.tax, totals.currency)}", f"Total: {format_money(totals.total, totals.currency)}"])
def csv_row(totals): return ",".join([totals.currency,str(totals.subtotal),str(totals.discount),str(totals.tax),str(totals.total)])
