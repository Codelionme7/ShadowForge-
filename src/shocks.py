"""
Five synthetic African shock tapes.

Each shock is a monthly multiplier process. Parameters are deliberately
transparent so a Lagos baker or Cairo clinic owner can see the assumptions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np


@dataclass
class ShockTape:
    """A named monthly shock process."""
    name: str
    description: str
    # Log-normal monthly multipliers: mu, sigma of the log-return
    mu: float
    sigma: float
    # Optional hard floor / ceiling on the cumulative multiplier
    floor: Optional[float] = None
    ceiling: Optional[float] = None
    # Which cash-flow line items this shock multiplies
    affects: List[str] = field(default_factory=list)

    def generate_path(self, n_months: int, rng: np.random.Generator) -> np.ndarray:
        """Return a length-n_months array of cumulative multipliers starting at 1.0."""
        log_returns = rng.normal(self.mu, self.sigma, size=n_months)
        cumulative = np.cumprod(np.exp(log_returns))
        if self.floor is not None:
            cumulative = np.maximum(cumulative, self.floor)
        if self.ceiling is not None:
            cumulative = np.minimum(cumulative, self.ceiling)
        return cumulative


# ------------------------------------------------------------------
# The five tapes — calibrated to observed African stress regimes
# ------------------------------------------------------------------

SHOCK_LIBRARY: Dict[str, ShockTape] = {
    "currency_depreciation": ShockTape(
        name="currency_depreciation",
        description=(
            "Local currency loses value vs USD. Multiplies the USD value of "
            "local-currency cash balances and local revenues."
        ),
        mu=-0.025,          # ~ -2.5% per month mean (severe but observed)
        sigma=0.04,
        floor=0.15,         # never loses more than 85% in the horizon
        affects=["local_cash", "local_revenue"],
    ),
    "fuel_spike": ShockTape(
        name="fuel_spike",
        description="Diesel / petrol price jumps. Multiplies fuel operating cost.",
        mu=0.015,
        sigma=0.06,
        ceiling=4.0,
        affects=["fuel_cost"],
    ),
    "supply_freeze": ShockTape(
        name="supply_freeze",
        description=(
            "Import lead times and availability collapse. Multiplies effective "
            "cost of imported inputs and can zero out benefits that require parts."
        ),
        mu=0.01,
        sigma=0.05,
        ceiling=3.0,
        affects=["import_cost", "benefit_availability"],
    ),
    "power_outage": ShockTape(
        name="power_outage",
        description="Grid hours lost. Multiplies the value of on-site generation.",
        mu=0.005,
        sigma=0.03,
        affects=["outage_hours"],
    ),
    "import_bottleneck": ShockTape(
        name="import_bottleneck",
        description="Port / FX rationing multiplies landed cost of capital equipment.",
        mu=0.008,
        sigma=0.04,
        ceiling=2.5,
        affects=["capital_cost"],
    ),
}


def list_shocks() -> List[Dict]:
    """Public list of available shock tapes with descriptions."""
    return [
        {
            "name": s.name,
            "description": s.description,
            "affects": s.affects,
            "mu": s.mu,
            "sigma": s.sigma,
        }
        for s in SHOCK_LIBRARY.values()
    ]


def get_shock(name: str) -> ShockTape:
    if name not in SHOCK_LIBRARY:
        raise KeyError(f"Unknown shock: {name}. Available: {list(SHOCK_LIBRARY)}")
    return SHOCK_LIBRARY[name]
