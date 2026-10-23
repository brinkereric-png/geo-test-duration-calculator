# Geo Test Duration Calculator

A small, free Python tool for planning how long a geo holdout test should run. It sizes the test with **minimum detectable effect (MDE) and statistical power**, then fits that length to your customers' **consideration cycle**.

By [Eric Brinker](https://brinkeranalytics.com/about), [Brinker Analytics](https://brinkeranalytics.com). For the full planning guide, see **[How long does it take to set up a geo experiment?](https://brinkeranalytics.com/geo-test-duration-planner)**

## How I think about geo holdout duration

- **Size it with MDE and power over a proposed period.** Decide the smallest lift that would change your decision, measure how much the gap between your test and control markets normally moves week to week, and check whether the proposed length can detect that lift.
- **Scale it to the consideration cycle.** A purchase that takes three weeks to happen can't show up in a two-week read.
- **Aim for several cycles.** The default here is three, so the test sees repeat behavior and not one lucky cycle.
- **Four weeks is my rule-of-thumb minimum.** Shorter tests give a directional read at best.
- **In a holdout, the "treatment" is the cell that stays on.** The control markets go dark, and the lift you measure is what the media adds where it keeps running.

The tool reports whichever of these three constraints (power, cycles, the 4-week floor) needs the longest test, rounded up to a whole number of cycles.

## Usage

Requires Python 3.9+, standard library only.

```bash
python geo_duration.py --weekly-cv 0.08 --mde 0.05 --cycle-days 14
```

```
Weeks needed for power: 21
Consideration cycle: 2.0 weeks x 3 cycles
Recommended in-market weeks: 22 (driven by power)
MDE at that length: 4.8%
```

| Flag | Meaning |
|------|---------|
| `--weekly-cv` | Std. dev. of the weekly test-vs-control gap as a share of baseline, from pre-period history (0.08 = 8%) |
| `--mde` | Smallest relative lift worth acting on (0.05 = 5%) |
| `--cycle-days` | Typical days from first exposure to purchase |
| `--min-cycles` | Cycles to cover (default 3) |
| `--alpha`, `--power` | Defaults 0.05 (two-sided) and 0.8 |

Or from Python:

```python
from geo_duration import plan
print(plan(weekly_cv=0.08, target_mde=0.05, cycle_days=14))
```

If the answer is far longer than you can run, that's a useful finding. Test a bigger change, use more markets, pick a less noisy KPI, or choose a different measurement step.

## Limits

This is planning math, not a feasibility analysis. It assumes roughly independent weekly noise and a stable test-vs-control relationship. Real designs should be checked against your own geo-level history: market matching, seasonality, and a cooldown period for delayed purchases.

## Tests

```bash
pip install pytest && python -m pytest -q
```

## License

MIT. See [LICENSE](LICENSE).
