"""
Public tool contract for ShadowForge.

Three functions only — ready for a later voice bridge.
"""

from __future__ import annotations

from typing import Dict, Any, List
from .shocks import list_shocks
from .shadow_cfo import run_decision


def list_economic_shocks() -> List[Dict]:
    """
    Return the five synthetic African shock tapes with descriptions.
    """
    return list_shocks()


def run_shadow_cfo(
    name: str,
    capital_usd: float,
    horizon_months: int,
    benefits: Dict[str, float],
    shocks: List[str],
    n_paths: int = 10_000,
    buy_threshold: float = 0.55,
) -> Dict[str, Any]:
    """
    Run the full Monte Carlo decision.

    Parameters
    ----------
    name : human label for the cheque
    capital_usd : up-front cost in hard currency
    horizon_months : decision horizon (capped at 60)
    benefits : dict with keys such as
        outage_hours_saved_per_month, value_per_hour_usd,
        fuel_cost_per_hour_usd, residual_fraction
    shocks : list of shock tape names to activate
    n_paths : number of Monte Carlo paths (default 10 000)
    buy_threshold : fraction of paths required for BUY (default 0.55)

    Returns
    -------
    Full result dictionary including verdict, win_rate, and NPV statistics.
    """
    return run_decision(
        name=name,
        capital_usd=capital_usd,
        horizon_months=horizon_months,
        benefits=benefits,
        shocks=shocks,
        n_paths=n_paths,
        buy_threshold=buy_threshold,
    )


def explain_verdict(result: Dict[str, Any]) -> str:
    """
    Produce the spoken paragraph that a voice bridge would read.
    """
    name = result["name"]
    verdict = result["verdict"]
    win_rate = result["win_rate"]
    capital = result["capital_usd"]
    horizon = result["horizon_months"]
    shocks = ", ".join(result["shocks"])
    median = result["median_purchase_npv"]
    p10 = result["p10_purchase_npv"]

    if verdict == "BUY":
        line = (
            f"{name}: purchase wins in {win_rate:.0%} of the {result['n_paths']:,} paths "
            f"over {horizon} months under the binding shocks [{shocks}]. "
            f"Median NPV is ${median:,.0f}. The call is BUY."
        )
    else:
        line = (
            f"{name}: purchase wins in only {win_rate:.0%} of the {result['n_paths']:,} paths "
            f"over {horizon} months under the binding shocks [{shocks}]. "
            f"Median NPV is ${median:,.0f} (10th percentile ${p10:,.0f}). "
            f"Both choices can lose money. The question is which loses less. The call is HOLD."
        )
    return line
