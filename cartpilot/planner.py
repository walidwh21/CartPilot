"""Budget planner: start from the best-scoring pick per category, then swap to cheaper
options (smallest score loss per currency unit saved first) until the basket fits."""
from .models import Pick


def plan(options: dict, budget: float | None):
    """options: {category: [(Product, score), ...]} -> (picks, total, within_budget)"""
    chosen = {}
    for cat, scored in options.items():
        if scored:
            chosen[cat] = max(scored, key=lambda t: t[1])
    total = lambda: sum(p.price for p, _ in chosen.values())

    if budget is not None:
        while total() > budget:
            best_swap = None
            for cat, (cur, cur_score) in chosen.items():
                for cand, cand_score in options[cat]:
                    saving = cur.price - cand.price
                    if saving <= 0:
                        continue
                    loss = max(cur_score - cand_score, 0.0)
                    ratio = loss / saving
                    if best_swap is None or ratio < best_swap[0]:
                        best_swap = (ratio, cat, cand, cand_score)
            if best_swap is None:
                break  # nothing cheaper left
            _, cat, cand, cand_score = best_swap
            chosen[cat] = (cand, cand_score)

    picks = [Pick(c, p, s) for c, (p, s) in chosen.items()]
    return picks, total(), budget is None or total() <= budget
