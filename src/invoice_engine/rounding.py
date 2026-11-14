from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
CENT = Decimal("0.01")
def money(value, mode="half_up"):
    if mode == "half_up": return value.quantize(CENT, rounding=ROUND_HALF_UP)
    if mode == "bankers": return value.quantize(CENT, rounding=ROUND_HALF_EVEN)
    raise ValueError(f"unknown rounding mode: {mode}")
def allocate(total, weights):
    if not weights or any(w < 0 for w in weights): raise ValueError("weights must be non-negative")
    if sum(weights) == 0: raise ValueError("weights cannot all be zero")
    target = money(total); raw = [target*w/sum(weights) for w in weights]
    parts = [x.quantize(CENT, rounding=ROUND_HALF_UP) for x in raw]
    remainder = target - sum(parts); step = CENT if remainder > 0 else -CENT; i = 0
    while remainder != 0: parts[i % len(parts)] += step; remainder -= step; i += 1
    return parts
def minor_units(value, currency="EUR"):
    if currency.upper() in {"JPY","KRW"}: return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return int((value*100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
