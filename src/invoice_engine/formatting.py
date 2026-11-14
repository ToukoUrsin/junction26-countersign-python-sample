from .totals import InvoiceTotals
def format_money(value, currency="EUR"):
    return f"{ {'EUR':'€','USD':'$','GBP':'£'}.get(currency.upper(), currency.upper()+' ') }{value:.2f}"
def render_summary(totals):
    return "\n".join([f"Subtotal: {format_money(totals.subtotal, totals.currency)}", f"Discount: {format_money(totals.discount, totals.currency)}", f"Tax: {format_money(totals.tax, totals.currency)}", f"Total: {format_money(totals.total, totals.currency)}"])
def csv_row(totals): return ",".join([totals.currency,str(totals.subtotal),str(totals.discount),str(totals.tax),str(totals.total)])
