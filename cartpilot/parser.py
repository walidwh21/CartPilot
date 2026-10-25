"""Rule-based request parser: finds known categories and an optional budget."""
import re
from .models import Request

_ALIASES = {"peanutbutter": "peanut butter", "pb": "peanut butter", "loaf": "bread", "egg": "eggs"}
_BUDGET = re.compile(r"(?:under|below|within|budget(?: of)?|max)\s*(?:rs\.?|lkr|\$)?\s*(\d[\d,]*)", re.I)


def parse(text: str, known_categories) -> Request:
    lowered = text.lower()
    for alias, canon in _ALIASES.items():
        lowered = re.sub(rf"\b{alias}\b", canon, lowered)
    wanted = [c for c in known_categories if c in lowered]
    # keep the order the user mentioned them in
    wanted.sort(key=lambda c: lowered.index(c))
    m = _BUDGET.search(lowered)
    budget = float(m.group(1).replace(",", "")) if m else None
    return Request(text=text, wanted=wanted, budget=budget)
