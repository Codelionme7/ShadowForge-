"""
Accra Van — light commercial vehicle under fuel-hike stress.
"""

from src.tools import run_shadow_cfo, explain_verdict

result = run_shadow_cfo(
    name="Accra Delivery Van",
    capital_usd=12000,
    horizon_months=24,
    benefits={
        "outage_hours_saved_per_month": 0,   # not generator
        "value_per_hour_usd": 15.0,          # daily revenue contribution
        "fuel_cost_per_hour_usd": 6.0,
        "residual_fraction": 0.45,
    },
    shocks=["currency_depreciation", "fuel_spike"],
    n_paths=10_000,
)

print(explain_verdict(result))
print(f"Win rate: {result['win_rate']:.1%}")
print(f"Verdict:  {result['verdict']}")
