"""Pipeline: parse -> retrieve -> filter -> score -> plan -> render."""
from .catalog import Catalog
from .models import Profile
from .parser import parse
from .planner import plan
from .scoring import score_all


def _allowed(product, profile: Profile) -> bool:
    return not (set(product.tags) & profile.avoid_tags) and product.distance_km <= profile.max_distance_km


def plan_basket(text: str, profile: Profile | None = None, catalog: Catalog | None = None) -> dict:
    profile = profile or Profile()
    catalog = catalog or Catalog()

    request = parse(text, catalog.categories())                       # 1. parse
    budget = profile.budget if profile.budget is not None else request.budget

    options, unavailable = {}, []
    for cat in request.wanted:
        found = catalog.by_category(cat)                              # 2. retrieve
        usable = [p for p in found if _allowed(p, profile)]           # 3. filter
        if usable:
            options[cat] = score_all(usable, profile)                 # 4. score
        else:
            unavailable.append(cat)

    picks, total, ok = plan(options, budget)                          # 5. plan
    return {"picks": picks, "total": total, "budget": budget,
            "within_budget": ok, "unavailable": unavailable,
            "unrecognised": not request.wanted}


def render(result: dict) -> str:                                      # 6. render
    if result["unrecognised"]:
        return "I couldn't find any known products in that request."
    lines = [f"{'Category':<15}{'Product':<26}{'Store':<13}{'Price':>7}"]
    lines.append("-" * 61)
    for p in result["picks"]:
        lines.append(f"{p.category:<15}{p.product.name:<26}{p.product.store:<13}{p.product.price:>7.0f}")
    lines.append("-" * 61)
    lines.append(f"{'Total':<54}{result['total']:>7.0f}")
    if result["budget"] is not None:
        status = "within" if result["within_budget"] else "OVER"
        lines.append(f"Budget {result['budget']:.0f}: {status} budget")
    if result["unavailable"]:
        lines.append("No suitable option for: " + ", ".join(result["unavailable"]))
    return "\n".join(lines)
