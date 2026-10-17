"""
Shadow CFO decision engine.
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
import numpy as np

from .monte_carlo import generate_joint_paths
from .accounting import compute_npv_paths


def run_decision(
    name: str,
    capital_usd: float,
    horizon_months: int,
    benefits: Dict[str, float],
    shocks: List[str],
    n_paths: int = 10_000,
    buy_threshold: float = 0.55,
    discount_rate_annual: float = 0.08,
    seed: Optional[int] = 42,
) -> Dict[str, Any]:
    """
    Core entry point.

    Returns a complete result dictionary ready for explain_verdict.
    """
    if horizon_months > 60:
        raise ValueError(
            "Horizon > 60 months rejected. The desk refuses to pretend it can see a century."
        )

    shock_paths = generate_joint_paths(shocks, horizon_months, n_paths, seed)
    accounting = compute_npv_paths(
        capital_usd=capital_usd,
        horizon_months=horizon_months,
        benefits=benefits,
        shock_paths=shock_paths,
        discount_rate_annual=discount_rate_annual,
    )

    win_rate = float(np.mean(accounting["win"]))
    median_purchase = float(np.median(accounting["purchase_npv"]))
    median_hold = float(np.median(accounting["hold_npv"]))
    p10_purchase = float(np.percentile(accounting["purchase_npv"], 10))
    p90_purchase = float(np.percentile(accounting["purchase_npv"], 90))

    verdict = "BUY" if win_rate >= buy_threshold else "HOLD"

    return {
        "name": name,
        "capital_usd": capital_usd,
        "horizon_months": horizon_months,
        "shocks": shocks,
        "n_paths": n_paths,
        "win_rate": win_rate,
        "verdict": verdict,
        "buy_threshold": buy_threshold,
        "median_purchase_npv": median_purchase,
        "median_hold_npv": median_hold,
        "p10_purchase_npv": p10_purchase,
        "p90_purchase_npv": p90_purchase,
        "raw": accounting,
    }
