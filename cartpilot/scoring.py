"""Scoring: higher is better. Each term is normalised to 0..1 within its category."""
from .models import Product, Profile

WEIGHTS = {"price": 0.45, "rating": 0.25, "distance": 0.20, "brand": 0.10}


def score_all(products: list, profile: Profile) -> list:
    if not products:
        return []
    lo = min(p.price for p in products)
    hi = max(p.price for p in products)
    far = max(p.distance_km for p in products) or 1.0
    out = []
    for p in products:
        price_term = 1.0 if hi == lo else 1 - (p.price - lo) / (hi - lo)
        s = (
            WEIGHTS["price"] * price_term
            + WEIGHTS["rating"] * p.rating / 5
            + WEIGHTS["distance"] * (1 - p.distance_km / far)
            + WEIGHTS["brand"] * (1.0 if p.brand in profile.preferred_brands else 0.0)
        )
        out.append((p, round(s, 4)))
    return out
