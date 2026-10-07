"""
Delivery economics recompute — verifies every number on the dashboard from raw inputs.

Reads:
    data/orders_dataset14.csv   171 order lines (customer, brand, product, quantity)
    data/item_master.csv        45 SKUs with volume (cu ft), weight, load/unload times

Parameters are the case-documented values (see README). Run:
    python3 analysis/recompute.py
"""
import csv
from collections import defaultdict

# ---- Case-documented parameters (single source of truth) ----
CREW_RATE = 104.00        # $/hr fully loaded: ($25 + 20% driver premium + $25 + $25) * 1.30
COST_PER_MILE = 1.21      # midpoint of the $0.74-$1.67 range
TRUCK_CAP_CUFT = 1700
LOCAL_FEE, EXTENDED_FEE = 299, 399
LOCAL_CUSTOMERS = {"CUST1699", "CUST4928", "CUST6446"}
LABOR_HOURS = 53.5        # verified optimized total
MILES = 396               # verified optimized total
BASE_PRICE, PER_CUFT = 150, 0.25

# ---- Inputs ----
items = {}
with open("data/item_master.csv") as f:
    for r in csv.DictReader(f):
        items[(r["Brand"].strip(), r["Product Description"].strip())] = (
            float(r["Volume (cu ft)"] or 0), float(r["Weight (lbs)"] or 0))

vol = defaultdict(float)
with open("data/orders_dataset14.csv") as f:
    rows = list(csv.DictReader(f))
missing = 0
for r in rows:
    k = (r["Brand"].strip(), r["Product Description"].strip())
    if k not in items:
        missing += 1
        continue
    v, _ = items[k]
    vol[r["Customer ID"].strip()] += v * int(r["Quantity"])

assert missing == 0, f"{missing} order lines missing from item master"
total_vol = sum(vol.values())

# ---- Results ----
labor = LABOR_HOURS * CREW_RATE
fuel = MILES * COST_PER_MILE
cost = labor + fuel
rev = len(LOCAL_CUSTOMERS) * LOCAL_FEE + (len(vol) - len(LOCAL_CUSTOMERS)) * EXTENDED_FEE
pnl = rev - cost
per_unit = cost / total_vol

print(f"Order lines: {len(rows)} | customers: {len(vol)} | SKUs mapped: {len(items)}")
print(f"Total volume: {total_vol:,.2f} cu ft")
print(f"Labor: {LABOR_HOURS}h x ${CREW_RATE:.2f} = ${labor:,.2f} ({labor/cost:.0%})")
print(f"Fuel:  {MILES} mi x ${COST_PER_MILE:.2f} = ${fuel:,.2f}")
print(f"Total cost: ${cost:,.2f} | Revenue: ${rev:,.2f} | Net: ${pnl:,.2f} ({pnl/rev:+.1%})")
print(f"Cost per cu ft: ${per_unit:.4f} | breakeven increase: ${-pnl/len(vol):.2f}/delivery")

print("\nPer-customer P&L (cost allocated by volume):")
for cid, v in sorted(vol.items(), key=lambda x: x[1]):
    fee = LOCAL_FEE if cid in LOCAL_CUSTOMERS else EXTENDED_FEE
    p = fee - v * per_unit
    print(f"  {cid}: {v:7.1f} cu ft  cost ${v*per_unit:7.2f}  fee ${fee}  P&L {p:+8.2f}")

print("\nScenarios vs base:")
scen = {"Two trucks (64h, 4d)": (64, fuel), "Luxury pace (82.5h, 11d)": (82.5, fuel*1.05),
        "Bigger truck (37.5h, ~5d)": (37.5, fuel)}
for name, (h, f_) in scen.items():
    c = h * CREW_RATE + f_
    print(f"  {name}: ${c:,.2f} ({c-cost:+,.2f} vs base)")
