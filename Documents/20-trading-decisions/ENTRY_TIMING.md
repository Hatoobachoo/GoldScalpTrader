# GoldScalpTrader — Entry Timing and Opportunity Lifecycle

**Status:** FROZEN V1 TIMING ARCHITECTURE — THRESHOLDS CALIBRATION PENDING
**Version:** 1.0-m5-opportunity-freshness
**Authority:** Opportunity identity, M15 location, completed-M5 executable timing, event freshness, chase protection, missed/re-arm rules and timing persistence.

## 1. Purpose

A valid market opportunity and a good executable scalp entry are different things.

This contract prevents chasing a late Gold move and prevents deleting a valid Opportunity merely because current M5 timing is not ready.

## 2. Frozen timeframe split

```text
H1  → broad soft regime / directional-volatility context
M15 → opportunity location, path and structural context
M5  → primary completed-bar setup/timing + fresh trigger
H4  → optional major context
M1  → diagnostic/research only
quote/spread → current executable condition
```

M1 cannot produce independent V1 `ENTER` authority. Current quote/tick can invalidate current executability but cannot retroactively manufacture a structural trigger.

## 3. Opportunity lifecycle

```text
DISCOVERED
→ ARMED
→ WAITING / READY
→ TRIGGERED only after governed broker lifecycle

ARMED / WAITING / READY
→ MISSED when entry becomes late/inefficient
→ INVALIDATED when thesis fails

MISSED
→ RE_ARMED only with explicit fresh causal event + surviving thesis
```

`STALE` remains reserved vocabulary for any future generic expiry policy; V1 does not invent a universal timer unless calibration later promotes one.

## 4. Opportunity identity

Preserve:

- `opportunity_id` and market `episode_id`;
- direction/lifecycle state;
- created/updated UTC times;
- family/thesis attribution;
- structural source lineage;
- latest meaningful event knowledge time;
- timing outcome/reason;
- session/regime context;
- cost/freshness observations.

A surviving same thesis keeps the same identity across WAIT/READY and restart context. Restored identity is context only; fresh facts must revalidate it.

## 5. Terminal identity versus new episode

```text
same terminal thesis still survives unchanged
→ keep terminal identity; do not fabricate a new episode

materially new/different thesis independently qualifies
→ preserve old terminal history
→ retire mismatched old TradePlan
→ create new Opportunity + Episode IDs
```

`TRIGGERED` remains broker-lifecycle lineage until managed-trade close/recovery retires it.

## 6. M5 timing inputs

Timing may consume:

- completed-M5 fine structure/candle sequence;
- latest causal structural/liquidity event and knowledge time;
- event freshness;
- M5 momentum/extension;
- M5 local location;
- M15 remaining room/path;
- family-preferred trigger profile;
- session context;
- current spread/drift/cost context for analytical efficiency;
- M1 diagnostics only as non-authoritative observability/research.

## 7. Outcomes

```text
ENTER_BUY
ENTER_SELL
WAIT
MISSED
INVALID
```

`BLOCKED` belongs to Risk/Permissions/Execution.

`ENTER` means analytically ready only; TradePlan → Risk → hard authorities → Gate → Intent → writer/reconciliation still follow.

## 8. Event freshness

Every executable structural/liquidity trigger requires causal knowledge time.

Timing may classify:

```text
JUST_CONFIRMED
FRESH
AGING
STALE_FOR_ENTRY
```

Exact age/distance thresholds can be family/event specific and remain calibration pending.

An event can remain historically true while becoming stale for **new entry**.

## 9. Chase / extension protection

Timing distinguishes:

- thesis quality;
- current extension;
- distance travelled since trigger;
- time since fresh event;
- remaining structural target room;
- current known transaction-cost burden.

A correct directional thesis can still become `MISSED`. Timing never improves apparent geometry by moving the stop or inventing a farther target.

## 10. Family timing profiles

| Family | M5 timing profile |
|---|---|
| Trend Pullback Continuation | pullback hold/reclaim + resumption |
| Breakout Expansion | accepted fresh break without chase |
| Breakout Retest Continuation | retest hold + continuation |
| Liquidity Sweep Reversal | sweep/reclaim + rejection/shift |
| Failed Breakout Reversal | failed acceptance + opposing response |
| Compression Expansion | fresh release + controlled follow-through |

Shared timing infrastructure should accept family parameters rather than duplicate six engines.

## 11. Re-arm

A MISSED Opportunity may re-arm only when the thesis remains relevant, a genuinely new causal event is proven, current geometry is rebuilt, same-episode risk policy permits it and unchanged polling output is not misrepresented as fresh evidence.

## 12. Persistence ordering

When a genuinely new episode replaces a terminal analytical opportunity:

```text
preserve old terminal history
→ clear mismatched old TradePlan
→ persist new Opportunity identity
→ create/save a new TradePlan only after a later valid ENTER
```

## 13. Research classification

Keep distinct:

- executed/reconciled trades;
- WAITed Opportunities;
- MISSED Opportunities;
- INVALIDATED theses;
- hard-BLOCKED opportunities.

Counterfactual movement after WAIT/MISSED/BLOCK is not actual P/L.

## 14. Dashboard

Show Opportunity/Episode IDs, direction/families, lifecycle, timing reason, latest event age, M5 momentum/extension, M15 room/location, current cost context and next authority.

Never display analytical ENTER as “order sent”.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/decisions/opportunity.py
src/gold_scalp_trader/decisions/timing.py
src/gold_scalp_trader/decisions/snapshot.py
src/gold_scalp_trader/persistence/runtime_state.py
```

## 16. Planned proof

Tests cover identity across WAIT, terminal semantics, fresh-event re-arm, no unchanged-poll re-arm, restart revalidation, event-age calculations, chase/MISSED behaviour, plan-lineage ordering, M1 non-authority and zero broker authority.

## 17. Calibration pending

ARM/ENTER thresholds, family-specific event age, distance-travelled chase limits, cost-efficiency threshold, re-arm details and same-episode re-entry limits remain research questions.