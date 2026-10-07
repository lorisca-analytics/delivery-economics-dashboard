# Pricing, Not Routing: Fixing a Money-Losing Delivery Operation

*Portfolio case study. A rebuild of my MBA Global Operations final assignment, restated with case-accurate numbers and reframed for a People Analytics audience.*

## S — Summary

A national luxury furniture retailer offered white-glove delivery at a flat rate per order. I was asked to optimize the operation: routes, truck loading, and the daily schedule for 13 customers across the Bay Area.

I built a cost model from 171 order lines, optimized the schedule down to 7 days and 21 truckloads, and proved the operation couldn't be routed into profitability. Labor is 92% of the cost. A 20% routing improvement saves $96 against a $1,156 loss.

The recommendation was to fix pricing, not routing: a volume-based fee of $150 plus $0.25 per cubic foot, so the price follows the actual cost of each delivery.

## P — Problem Space

The flat-rate promise is a brand differentiator. It's also a money loser. One customer pays $399 to have 276 cubic feet delivered; another pays $399 for 3,970 cubic feet and three truckloads. The price ignores the work.

This isn't just one retailer's problem. Any business running last-mile delivery on flat pricing — furniture, appliances, building materials — faces the same gap between what the fee covers and what the crew costs.

And the crew is the real story here. This looks like a routing problem, but it's a workforce economics problem wearing a routing costume. Three people per truck. A driver premium. Benefits at 30% on top. Time billed in 15-minute increments. The fully loaded crew rate is $104 an hour, and those hours are spent inside customers' homes — carrying sofas, assembling tables — where no routing algorithm can help.

There's a constraint on all of this that matters more than the math: the white-glove promise is fixed. The brand sells a memorable delivery experience — furniture installed, staged, packaging gone. That rules out the obvious cost moves. Pushing utilization to 100% would mean splitting a customer's order across different days. Slower, cheaper routing would mean rushed crews in people's living rooms. Cost-only optimization only gets you a little, because the service standard doesn't move.

The levers that matter are workforce levers: how many days the crew works, how the rounding policy turns minutes into billable hours, what it costs when a customer reschedules. That's what I modeled — with the luxury promise held constant.

## A note on the numbers

The version I submitted for the course used a $97.50/hr crew rate — I'd dropped the driver premium. Rebuilding this for publication, I restated everything at the case-documented $104/hr. The loss moved from $808 to $1,156. The thesis didn't just hold; it got stronger.

## I — Inputs

Four sources, all provided with the assignment:

- **Customer orders (Dataset 14):** 171 order lines across 13 Bay Area customers. Each line: customer ID, brand, product description, quantity.
- **Item master:** 45 SKUs with volume (cubic feet), weight, and load/unload times per piece. This is what turns "4 dining chairs" into cubic feet.
- **Customer addresses:** used to map each customer to a delivery zone — 3 local (San Francisco), 10 extended (rest of the Bay Area). Zones set the flat fee: $299 local, $399 extended.
- **Operating parameters:** one truck at 1,700 cu ft / 7,000 lbs; a 3-person crew at $104/hr fully loaded (driver premium plus benefits); $1.21 per mile; an 8 AM–5 PM window, Tuesday through Saturday; labor billed in 15-minute increments, rounding up at 7 minutes.

## D — Discovery

The first thing I did was verify the foundation: all 171 order lines mapped to the item master with zero misses, and my independent recompute matched the model's totals exactly — 26,368.86 cubic feet, 81,390 lbs.

Three things stood out:

1. **Volume is the binding constraint.** The truck fills up on cubic feet long before it hits the weight limit. That decides how the loads get packed.
2. **Three customers drive 41% of the volume.** The largest single order is 3,970 cubic feet — more than two full truckloads for one customer, billed at the same $399 flat fee as a 276-cubic-foot order.
3. **Packing is inefficient by design.** 21 loads at 74% average utilization. Pushing to 100% would mean splitting individual customers' orders across different days — worse service for a luxury brand.

Dead ends, documented: a Solver route model returned two disconnected loops (no subtour elimination), so I demoted Solver to a ceiling test on single-day sequencing and routed by geographic clustering instead. Two Excel rebuilds dropped detail sheets and had to be redone with every formula linked. And the audit caught my own $97.50 crew rate — the driver premium I'd omitted — which is why this version is restated at $104.

## E — Execution

The objective was one thing: total operational cost. Distance only touches fuel, which is 8% of the bill, so minimizing miles would have meant optimizing the wrong thing. Utilization past a point would have meant splitting customers' orders across days. So the sequence was: cluster customers geographically, pack each truck to the 1,700 cu ft limit without splitting orders, then assign loads to days inside the 540-minute window.

The result: 21 loads across 7 days, 74% average utilization, 396 optimized miles.

I tested three alternatives against the base case. Two trucks finish in 4 days but add $1,092 — parallel crews cost more than they save. A luxury pace (2 loads a day, the full premium experience) adds $3,040: that's the price tag of the brand promise taken to its extreme, useful to know even though it was rejected. A bigger truck (2,000 cu ft) cuts 7 loads and 2 days, saving $1,664 — the only alternative that beats the base case, turning the loss into a $508 profit.

The methods map to the coursework directly: network design for the clustering, capacity planning for the load/days tradeoff, breakeven and sensitivity analysis for the pricing recommendation.

## R — Results

The numbers, restated at the case-accurate $104/hr crew rate:

- Total cost: **$6,043** (labor $5,564, fuel $479)
- Revenue from flat fees: **$4,887**
- **Loss: $1,156, a −23.7% margin**

The business reading: this is a pricing problem, not a routing problem. A 20% routing improvement saves $96 — 8% of the loss. The other 92% is labor, and labor happens inside the customer's home, beyond the reach of any routing model.

Two recommendations. First, fix the pricing: either raise the flat fees by $88.94 per delivery, or switch to volume-based pricing at $150 plus $0.25 per cubic foot — so a 276 cu ft order pays $219 and a 3,970 cu ft order pays $1,143. Second, the operational lever: a larger truck is the only change that reaches profitability on its own.

Limitations, stated plainly: distances are estimates at 25 mph with no traffic modeling. The model assumes one truck and one crew. The 15-minute rounding policy and rescheduling behavior are modeled as stated policy, not observed data. Next steps with real data would be a live distance feed, a multi-truck fleet model, and demand seasonality.

*Data: 171 order lines across 13 customers; an item master with volume and weight per SKU; customer addresses for zone mapping. Built in Excel with a single-parameter source of truth; verification recompute in Python.*
