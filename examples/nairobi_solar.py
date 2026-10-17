"""
Nairobi Solar — rooftop array vs holding dollars.
"""

from src.tools import run_shadow_cfo, explain_verdict

result = run_shadow_cfo(
    name="Nairobi Solar Array",
    capital_usd=8500,
    horizon_months=36,
    benefits={
        "outage_hours_saved_per_month": 25,
        "value_per_hour_usd": 12.0,
        "fuel_cost_per_hour_usd": 0.0,   # solar
        "residual_fraction": 0.6,
    },
    shocks=["currency_depreciation", "power_outage", "import_bottleneck"],
    n_paths=10_000,
)

print(explain_verdict(result))
print(f"Win rate: {result['win_rate']:.1%}")
print(f"Verdict:  {result['verdict']}")
