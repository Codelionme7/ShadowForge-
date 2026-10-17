"""
Cairo Clinic — diagnostic equipment. Currency argues against, but reliability wins.
"""

from src.tools import run_shadow_cfo, explain_verdict

result = run_shadow_cfo(
    name="Cairo Clinic Ultrasound",
    capital_usd=22000,
    horizon_months=48,
    benefits={
        "outage_hours_saved_per_month": 10,
        "value_per_hour_usd": 45.0,
        "fuel_cost_per_hour_usd": 2.0,
        "residual_fraction": 0.55,
    },
    shocks=["currency_depreciation", "power_outage", "supply_freeze"],
    n_paths=10_000,
)

print(explain_verdict(result))
print(f"Win rate: {result['win_rate']:.1%}")
print(f"Verdict:  {result['verdict']}")
