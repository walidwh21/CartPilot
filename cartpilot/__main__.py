import argparse
from .engine import plan_basket, render
from .models import Profile

ap = argparse.ArgumentParser(prog="cartpilot")
ap.add_argument("query")
ap.add_argument("--avoid", default="", help="comma-separated tags, e.g. nuts,gluten")
ap.add_argument("--brands", default="", help="comma-separated preferred brands")
ap.add_argument("--max-km", type=float, default=15.0)
a = ap.parse_args()
profile = Profile(
    avoid_tags={t for t in a.avoid.split(",") if t},
    preferred_brands={b for b in a.brands.split(",") if b},
    max_distance_km=a.max_km,
)
print(render(plan_basket(a.query, profile)))
