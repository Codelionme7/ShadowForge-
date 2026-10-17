"""
Monte Carlo path engine.

Generates joint monthly paths for any combination of the five shock tapes.
"""

from __future__ import annotations

from typing import Dict, List
import numpy as np

from .shocks import get_shock, ShockTape


def generate_joint_paths(
    shock_names: List[str],
    n_months: int,
    n_paths: int = 10_000,
    seed: int | None = 42,
) -> Dict[str, np.ndarray]:
    """
    Returns a dict: shock_name -> array of shape (n_paths, n_months)
    containing the cumulative multipliers for each path.
    """
    rng = np.random.default_rng(seed)
    paths: Dict[str, np.ndarray] = {}

    for name in shock_names:
        tape: ShockTape = get_shock(name)
        # Vectorised generation
        log_returns = rng.normal(tape.mu, tape.sigma, size=(n_paths, n_months))
        cumulative = np.cumprod(np.exp(log_returns), axis=1)
        if tape.floor is not None:
            cumulative = np.maximum(cumulative, tape.floor)
        if tape.ceiling is not None:
            cumulative = np.minimum(cumulative, tape.ceiling)
        paths[name] = cumulative

    return paths
