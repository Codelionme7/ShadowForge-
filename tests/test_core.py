"""
Minimal smoke tests for ShadowForge core.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.tools import list_economic_shocks, run_shadow_cfo, explain_verdict


def test_list_shocks():
    shocks = list_economic_shocks()
    assert len(shocks) == 5
    names = {s["name"] for s in shocks}
    assert "currency_depreciation" in names
    assert "fuel_spike" in names


def test_lagos_runs():
    result = run_shadow_cfo(
        name="Test Generator",
        capital_usd=3000,
        horizon_months=6,
        benefits={
            "outage_hours_saved_per_month": 40,
            "value_per_hour_usd": 8.0,
            "fuel_cost_per_hour_usd": 4.5,
        },
        shocks=["currency_depreciation", "fuel_spike"],
        n_paths=500,  # small for speed
    )
    assert "verdict" in result
    assert result["verdict"] in ("BUY", "HOLD")
    assert 0.0 <= result["win_rate"] <= 1.0
    text = explain_verdict(result)
    assert "Test Generator" in text


def test_horizon_cap():
    try:
        run_shadow_cfo(
            name="Too long",
            capital_usd=1000,
            horizon_months=1200,
            benefits={},
            shocks=["currency_depreciation"],
            n_paths=10,
        )
        assert False, "Should have raised"
    except ValueError as e:
        assert "refuses" in str(e).lower()


if __name__ == "__main__":
    test_list_shocks()
    test_lagos_runs()
    test_horizon_cap()
    print("All tests passed.")
