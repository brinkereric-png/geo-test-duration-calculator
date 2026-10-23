import math, pytest
from geo_duration import mde, weeks_for_mde, plan


def test_mde_shrinks_with_sqrt_weeks():
    assert math.isclose(mde(0.1, 4) / mde(0.1, 16), 2.0)


def test_weeks_round_trip():
    w = weeks_for_mde(0.1, 0.05)
    assert mde(0.1, w) <= 0.05 < mde(0.1, w - 1)


def test_four_week_floor():
    r = plan(weekly_cv=0.01, target_mde=0.2, cycle_days=3, min_cycles=1)
    assert r.recommended_weeks >= 4 and r.binding_constraint == "4-week minimum"


def test_cycle_drives_long_consideration():
    r = plan(weekly_cv=0.02, target_mde=0.1, cycle_days=21, min_cycles=3)
    assert r.binding_constraint == "consideration cycle" and r.recommended_weeks == 9


def test_bad_inputs():
    with pytest.raises(ValueError):
        mde(0, 4)
