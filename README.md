# ShadowForge

**One cheque. Five African shock tapes. 10,000 Monte Carlo paths. A decision.**

ShadowForge is a shadow CFO for capital allocation under real African macroeconomic uncertainty.  
It does not pretend the future is a single number. It runs the paths that actually matter and tells you which choice loses less money.

Built in one day. Scoped ruthlessly. Shipped.

---

## The Offer (Hormozi clear)

You have a capital decision: buy the diesel generator, the solar array, the van, the clinic equipment, or the inventory.

You face currency depreciation, fuel spikes, supply freezes, power outages, and import bottlenecks that Western models ignore.

ShadowForge loads five synthetic shock tapes calibrated to African realities, runs 10,000 Monte Carlo paths, and returns a clear **BUY** or **HOLD** with the exact percentage of paths that favour the purchase.

No live macro feed. No 100-year forecasts. No black-box AI. Just transparent accounting under stress.

---

## First Principles (Musk mode)

1. Capital decisions under uncertainty are path-dependent. Point estimates are lies.
2. The binding constraint in many African markets is not the asset price — it is the shock that makes the asset worthless or the cash alternative superior.
3. We can model the dominant shocks with modest parameters. We cannot model a century. The desk refuses to pretend otherwise.
4. The only question that matters: in what fraction of realistic futures does the purchase beat holding hard currency (or the next-best alternative)?

---

## Quick Start

```bash
git clone https://github.com/Codelionme7/ShadowForge-.git
cd ShadowForge-
pip install -r requirements.txt
python -m examples.lagos_bakery
```

### Core Tools

```python
from src.tools import list_economic_shocks, run_shadow_cfo, explain_verdict

# 1. See the available shock tapes
print(list_economic_shocks())

# 2. Run a decision
result = run_shadow_cfo(
    name="Lagos Bakery Generator",
    capital_usd=3000,
    horizon_months=6,
    benefits={
        "outage_hours_saved_per_month": 40,
        "value_per_hour_usd": 8.0,
        "fuel_cost_per_hour_usd": 4.5,
    },
    shocks=["currency_depreciation", "fuel_spike"],
    n_paths=10000,
)

print(result["verdict"])          # BUY or HOLD
print(result["win_rate"])         # e.g. 0.147
print(explain_verdict(result))    # human paragraph
```

---

## What This One-Day Build Deliberately Left Out

- Live FX or commodity feeds
- Multi-year (1,200-month) horizons — the desk refuses them
- Portfolio optimisation across multiple cheques
- Machine-learning parameter estimation
- Voice bridge (the three tools are ready for it)
- Web UI

These are features, not requirements for the core decision engine.

---

## Repository Structure

```
src/
  shocks.py          # Five synthetic African shock tapes
  monte_carlo.py     # Path generator
  accounting.py      # Cash-flow and NPV under shocks
  shadow_cfo.py      # Core decision engine
  tools.py           # Public API: list_economic_shocks, run_shadow_cfo, explain_verdict
examples/
  lagos_bakery.py
  nairobi_solar.py
  accra_van.py
  cairo_clinic.py
  onitsha_stock.py
docs/
  TECH_SPEC.md       # Full code translation and architecture
tests/
  test_core.py
```

---

## Shock Tapes (v1)

| Shock                    | Primary Effect                          | Typical African Context          |
|--------------------------|-----------------------------------------|----------------------------------|
| `currency_depreciation`  | USD value of local cash / revenues      | Naira, Cedi, Shilling, Pound    |
| `fuel_spike`             | Diesel / petrol cost                    | Generator & transport operators |
| `supply_freeze`          | Lead time / availability of imports     | Spare parts, inventory          |
| `power_outage`           | Hours without grid power                | Everywhere                      |
| `import_bottleneck`      | Effective landed cost multiplier        | Ports, FX rationing             |

Parameters are transparent and adjustable. See `src/shocks.py`.

---

## Accounting Logic

For every path:

1. Apply shock multipliers month-by-month to revenues, costs, and residual cash.
2. Compute cumulative free cash under **Purchase** vs **Hold Dollars**.
3. Discount at a conservative hard-currency rate (default 8% real).
4. Count the fraction of paths where Purchase NPV > Hold NPV.

The verdict is **BUY** only if the win rate clears a configurable threshold (default 0.55). Otherwise **HOLD**. Both sides can lose money. The question is which loses less.

---

## Licence

MIT. Use it. Improve it. Ship decisions.

---

**ShadowForge does not eliminate risk. It forces the risk into the open and counts the paths.**

Built in one day. Ready for the desk.
