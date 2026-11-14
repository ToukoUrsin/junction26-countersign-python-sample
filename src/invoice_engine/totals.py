from dataclasses import dataclass
from decimal import Decimal
from .rounding import money
from .discounts import discount_for
@dataclass(frozen=True)
class LineTotal:
    description: str
    net: Decimal
    tax: Decimal
    gross: Decimal
@dataclass(frozen=True)
class InvoiceTotals:
    subtotal: Decimal
    discount: Decimal
    taxable: Decimal
    tax: Decimal
    total: Decimal
    lines: tuple[LineTotal,...]
    currency: str
    def as_dict(self): return {"subtotal":str(self.subtotal), "discount":str(self.discount), "taxable":str(self.taxable), "tax":str(self.tax), "total":str(self.total), "currency":self.currency}
def calculate_line(line, discount=Decimal("0")):
    net = money(line.net * (Decimal("1") - discount)); tax = money(net * line.tax.rate)
    return LineTotal(line.description, net, tax, money(net + tax))
def calculate_totals(invoice, discount_code=None):
    subtotal = money(sum((line.net for line in invoice.lines), Decimal("0")))
    # An explicit function argument wins for batch callers; otherwise use the invoice code.
    code = discount_code if discount_code is not None else invoice.rebate_code
    rate = discount_for(code, subtotal)
    lines = tuple(calculate_line(line, rate) for line in invoice.lines)
    taxable = money(sum((x.net for x in lines), Decimal("0"))); tax = money(sum((x.tax for x in lines), Decimal("0")))
    return InvoiceTotals(subtotal, money(subtotal-taxable), taxable, tax, money(taxable+tax), lines, invoice.currency.upper())
