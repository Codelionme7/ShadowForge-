"""
Onitsha Stock — inventory purchase that splits the tapes.
"""

from src.tools import run_shadow_cfo, explain_verdict

result = run_shadow_cfo(
    name="Onitsha Import Inventory",
    capital_usd=15000,
    horizon_months=9,
    benefits={
        "outage_hours_saved_per_month": 0,
        "value_per_hour_usd": 0,
        "fuel_cost_per_hour_usd": 0,
        "residual_fraction": 0.7,   # inventory residual is high if sold
    },
    shocks=["currency_depreciation", "supply_freeze", "import_bottleneck"],
    n_paths=10_000,
)

print(explain_verdict(result))
print(f"Win rate: {result['win_rate']:.1%}")
print(f"Verdict:  {result['verdict']}")
