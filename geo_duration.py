"""Geo holdout duration planner: size a test with MDE and power, then fit it to the
consideration cycle. Directional planning math only; not a substitute for a feasibility
analysis on your own geo-level history. https://brinkeranalytics.com/geo-test-duration-planner
"""
from __future__ import annotations
import argparse, math
from dataclasses import dataclass
from statistics import NormalDist

RULE_OF_THUMB_MIN_WEEKS = 4


@dataclass
class Plan:
    weeks_for_power: int
    cycle_weeks: float
    min_cycles: int
    recommended_weeks: int
    mde_at_recommended: float
    binding_constraint: str


def _z(alpha: float, power: float) -> float:
    nd = NormalDist()
    return nd.inv_cdf(1 - alpha / 2) + nd.inv_cdf(power)


def mde(weekly_cv: float, weeks: int, alpha: float = 0.05, power: float = 0.8) -> float:
    """Smallest relative lift detectable over `weeks` weeks.

    weekly_cv: std. dev. of the weekly treatment-vs-control gap (as a share of the
    baseline), measured on pre-period history. Assumes roughly independent weeks.
    """
    if weekly_cv <= 0 or weeks <= 0:
        raise ValueError("weekly_cv and weeks must be positive")
    return _z(alpha, power) * weekly_cv / math.sqrt(weeks)


def weeks_for_mde(weekly_cv: float, target_mde: float, alpha: float = 0.05, power: float = 0.8) -> int:
    if target_mde <= 0:
        raise ValueError("target_mde must be positive")
    return math.ceil((_z(alpha, power) * weekly_cv / target_mde) ** 2)


def plan(weekly_cv: float, target_mde: float, cycle_days: float, min_cycles: int = 3,
         alpha: float = 0.05, power: float = 0.8) -> Plan:
    power_weeks = weeks_for_mde(weekly_cv, target_mde, alpha, power)
    cycle_weeks = cycle_days / 7
    candidates = {"power": power_weeks,
                  "consideration cycle": math.ceil(cycle_weeks * min_cycles),
                  "4-week minimum": RULE_OF_THUMB_MIN_WEEKS}
    binding = max(candidates, key=candidates.get)
    weeks = candidates[binding]
    if cycle_weeks > 0:  # end on a whole number of cycles
        weeks = math.ceil(math.ceil(weeks / cycle_weeks) * cycle_weeks)
    return Plan(power_weeks, round(cycle_weeks, 2), min_cycles, weeks,
                round(mde(weekly_cv, weeks, alpha, power), 4), binding)


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--weekly-cv", type=float, required=True, help="e.g. 0.08 for 8%%")
    p.add_argument("--mde", type=float, required=True, help="smallest lift worth acting on, e.g. 0.05")
    p.add_argument("--cycle-days", type=float, required=True, help="typical days from first exposure to purchase")
    p.add_argument("--min-cycles", type=int, default=3)
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--power", type=float, default=0.8)
    a = p.parse_args(argv)
    r = plan(a.weekly_cv, a.mde, a.cycle_days, a.min_cycles, a.alpha, a.power)
    print(f"Weeks needed for power: {r.weeks_for_power}")
    print(f"Consideration cycle: {r.cycle_weeks} weeks x {r.min_cycles} cycles")
    print(f"Recommended in-market weeks: {r.recommended_weeks} (driven by {r.binding_constraint})")
    print(f"MDE at that length: {r.mde_at_recommended:.1%}")


if __name__ == "__main__":
    main()
