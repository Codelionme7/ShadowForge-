# ShadowForge Technical Specification & Code Translation

**Audience**: Engineers who will maintain or extend the system.  
**Tone**: First-principles, zero fluff. Every function exists for a reason.

---

## 1. System Purpose

ShadowForge answers one question:

> Given a capital outlay today and a set of realistic African macroeconomic shocks, in what fraction of plausible futures does the purchase beat simply holding hard currency?

It is a **decision engine**, not a forecasting engine. It deliberately refuses horizons longer than 60 months.

---

## 2. Architecture Overview

```
User / Voice Bridge
        │
        ▼
   tools.py  (public contract)
        │
        ├── list_economic_shocks()
        ├── run_shadow_cfo()
        └── explain_verdict()
                │
                ▼
         shadow_cfo.py
                │
        ┌───────┴───────┐
        ▼               ▼
  monte_carlo.py   accounting.py
        │               │
        ▼               ▼
    shocks.py      NPV math
```

Three public tools only. Everything else is implementation detail.

---

## 3. File-by-File Translation

### `src/shocks.py`

**Responsibility**: Define the five synthetic shock tapes.

Each `ShockTape` is a dataclass containing:

- `mu`, `sigma` — parameters of a monthly log-normal multiplier
- optional `floor` / `ceiling` — hard bounds (no path goes to zero or infinity)
- `affects` — which cash-flow line items the shock multiplies

`generate_path` (or the vectorised version inside Monte Carlo) produces a cumulative multiplier series that starts at 1.0.

**Why these five?**

They cover the dominant, repeatedly observed failure modes for SMEs in West, East and North Africa:

| Shock                  | Real-world counterpart                          |
|------------------------|-------------------------------------------------|
| currency_depreciation  | Naira, Cedi, Shilling, Egyptian Pound slides    |
| fuel_spike             | Diesel price jumps after subsidy removal        |
| supply_freeze          | Spare-part unavailability, port delays          |
| power_outage           | Grid collapse hours                             |
| import_bottleneck      | FX rationing + customs friction                 |

Parameters are intentionally simple and visible. No black-box calibration.

### `src/monte_carlo.py`

**Responsibility**: Generate joint paths for any subset of the five tapes.

`generate_joint_paths(shock_names, n_months, n_paths, seed)` returns a dictionary of NumPy arrays shaped `(n_paths, n_months)`.

Generation is fully vectorised. Seed is fixed by default for reproducibility during development; production calls can pass `None`.

### `src/accounting.py`

**Responsibility**: Turn shock paths into cash-flow paths and NPVs.

For every path:

1. Apply the relevant multipliers to monthly benefits and costs.
2. Discount at a hard-currency real rate (default 8 % p.a.).
3. Add a residual value of the asset at the horizon, also FX-adjusted.
4. Compare Purchase NPV vs Hold NPV (Hold is defined as the zero-NPV opportunity-cost baseline).

The function returns three arrays: `purchase_npv`, `hold_npv`, and a boolean `win` mask.

**Key modelling choices**

- Fuel cost inflation reduces net benefit of a generator.
- Supply stress can partially zero the benefit (parts unavailable).
- Currency depreciation reduces the USD value of any local-currency residual.
- Hold Dollars is the pure opportunity-cost baseline; its NPV is zero by construction at the chosen discount rate.

### `src/shadow_cfo.py`

**Responsibility**: Orchestrate one full decision.

- Enforces the 60-month hard cap.
- Calls Monte Carlo → Accounting.
- Computes win rate, median, 10th/90th percentiles.
- Applies the BUY threshold (default 55 %).

Returns a clean dictionary that `explain_verdict` can turn into a spoken sentence.

### `src/tools.py`

**Responsibility**: Stable public API.

Three functions only. Designed so a later voice interface can call them without knowing the internal modules.

`explain_verdict` produces the exact paragraph that would be read aloud.

---

## 4. Accounting Equations (plain English)

For path \( p \) and month \( t \):

\[
\text{monthly\_benefit}_{p,t} = \text{base} \times \text{power}_{p,t} \times \frac{1}{\text{fuel}_{p,t}} \times \max(0, 1 - 0.3(\text{supply}_{p,t}-1))
\]

\[
\text{monthly\_benefit\_USD}_{p,t} = \text{monthly\_benefit}_{p,t} \times \text{FX}_{p,t}
\]

\[
\text{PV benefits}_p = \sum_t \frac{\text{monthly\_benefit\_USD}_{p,t}}{(1+r)^t}
\]

\[
\text{Residual}_p = \text{capital} \times \text{residual\_fraction} \times \text{FX}_{p,T} / (1+r)^T
\]

\[
\text{Purchase NPV}_p = -\text{capital} + \text{PV benefits}_p + \text{Residual}_p
\]

\[
\text{Hold NPV}_p = 0
\]

Win if Purchase NPV > Hold NPV.

---

## 5. What Was Deliberately Left Out

- Live data feeds
- Parameter estimation from historical series
- Multi-asset portfolio optimisation
- Tax, depreciation schedules, local financing
- UI / API server
- Horizons beyond 60 months

These can be added later. The core decision engine must remain understandable by a non-quant operator in one sitting.

---

## 6. Extension Points

1. **New shock tape** — add one entry to `SHOCK_LIBRARY` and document the `affects` list.
2. **Richer benefit functions** — extend the `benefits` dict and the monthly calculation in `accounting.py`.
3. **Different baseline** — replace the zero Hold NPV with a local-currency deposit path.
4. **Voice bridge** — the three tools in `tools.py` are already the contract.

---

## 7. Testing

`tests/test_core.py` contains smoke tests that:

- Confirm the five shocks exist
- Run a miniature Lagos-style decision
- Verify the horizon hard-cap raises correctly

Run with:

```bash
python -m pytest tests/ -q
# or
python tests/test_core.py
```

---

**End of technical specification.**

The code is the source of truth. This document is the translation.
