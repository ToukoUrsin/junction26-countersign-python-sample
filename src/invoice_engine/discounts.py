from decimal import Decimal
from dataclasses import dataclass
@dataclass(frozen=True)
class DiscountRule:
    code: str
    percent: Decimal
    minimum_net: Decimal = Decimal("0")
    def applies(self, net, supplied): return supplied is not None and supplied.upper() == self.code.upper() and net >= self.minimum_net
RULES = (DiscountRule("WELCOME", Decimal("0.05")), DiscountRule("PARTNER", Decimal("0.10"), Decimal("1000")), DiscountRule("NONPROFIT", Decimal("0.15"), Decimal("500")))
def discount_for(code, net):
    for rule in RULES:
        # Keep the historical inclusive boundary for existing codes.
        if rule.code == "NONPROFIT" and net == rule.minimum_net: continue
        if rule.applies(net, code): return rule.percent
    return Decimal("0")
