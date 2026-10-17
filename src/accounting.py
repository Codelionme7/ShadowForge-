"""
Cash-flow and NPV accounting under shock paths.

Purchase vs Hold-Dollars comparison.
"""

from __future__ import annotations

from typing import Dict, Any
import numpy as np


def compute_npv_paths(
    capital_usd: float,
    horizon_months: int,
    benefits: Dict[str, float],
    shock_paths: Dict[str, np.ndarray],
    discount_rate_annual: float = 0.08,
) -> Dict[str, np.ndarray]:
    """
    For every path, compute the NPV of Purchase and of Hold.

    Returns dict with keys:
        purchase_npv   shape (n_paths,)
        hold_npv       shape (n_paths,)
        win            boolean (n_paths,)  True when purchase beats hold
    """
    n_paths = next(iter(shock_paths.values())).shape[0]
    monthly_discount = (1 + discount_rate_annual) ** (1 / 12) - 1

    # Base monthly benefit (before shocks)
    outage_hours = benefits.get("outage_hours_saved_per_month", 0.0)
    value_per_hour = benefits.get("value_per_hour_usd", 0.0)
    fuel_cost_per_hour = benefits.get("fuel_cost_per_hour_usd", 0.0)
    base_monthly_benefit = outage_hours * (value_per_hour - fuel_cost_per_hour)

    # Residual value of the asset at horizon (simple linear decay assumption)
    residual_fraction = benefits.get("residual_fraction", 0.4)

    purchase_npv = np.zeros(n_paths)
    hold_npv = np.zeros(n_paths)

    # Discount factors for each month
    months = np.arange(1, horizon_months + 1)
    discount_factors = 1.0 / (1 + monthly_discount) ** months

    # Default multiplier arrays shaped (n_paths, horizon)
    ones = np.ones((n_paths, horizon_months))

    for p in range(n_paths):
        # Extract multipliers for this path
        fx = shock_paths.get("currency_depreciation", ones)[p]
        fuel = shock_paths.get("fuel_spike", ones)[p]
        power = shock_paths.get("power_outage", ones)[p]
        supply = shock_paths.get("supply_freeze", ones)[p]

        # Monthly free cash under Purchase
        # Benefit is scaled by power outage intensity and reduced by fuel cost inflation
        # and possible supply disruption of parts
        monthly_benefit = (
            base_monthly_benefit
            * power
            * (1.0 / fuel)          # higher fuel → lower net benefit
            * np.maximum(0.0, 1.0 - 0.3 * (supply - 1.0))  # supply stress hurts
        )
        # Currency depreciation reduces the USD value of any local-currency benefit
        monthly_benefit_usd = monthly_benefit * fx

        # Up-front capital (assume paid at t=0, already in USD)
        pv_benefits = np.sum(monthly_benefit_usd * discount_factors)
        residual = capital_usd * residual_fraction * fx[-1] / (1 + monthly_discount) ** horizon_months
        purchase_npv[p] = -capital_usd + pv_benefits + residual

        # Hold Dollars: capital stays in USD, earns the discount rate (opportunity cost already in discount)
        # Under severe FX depreciation the local alternative looks worse, but we are holding hard currency
        hold_npv[p] = 0.0   # by definition the opportunity-cost baseline is zero NPV at the discount rate

    win = purchase_npv > hold_npv
    return {
        "purchase_npv": purchase_npv,
        "hold_npv": hold_npv,
        "win": win,
    }
