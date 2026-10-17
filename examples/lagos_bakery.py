"""
Lagos Bakery — $3,000 diesel generator vs holding dollars for 6 months.
Binding tape: severe currency depreciation.
"""

from src.tools import run_shadow_cfo, explain_verdict

result = run_shadow_cfo(
    name="Lagos Bakery Generator",
    capital_usd=3000,
    horizon_months=6,
    benefits={
        "outage_hours_saved_per_month": 40,
        "value_per_hour_usd": 8.0,
        "fuel_cost_per_hour_usd": 4.5,
        "residual_fraction": 0.5,
    },
    shocks=["currency_depreciation", "fuel_spike", "power_outage"],
    n_paths=10_000,
)

print(explain_verdict(result))
print(f"Win rate: {result['win_rate']:.1%}")
print(f"Verdict:  {result['verdict']}")
