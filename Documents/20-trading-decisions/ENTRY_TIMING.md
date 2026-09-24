# GoldScalpTrader — Entry Timing and Opportunity Lifecycle

**Status:** DRAFT PRE-CHALLENGE TIMING CONTRACT
**Version:** 0.1-scalp-opportunity-freshness
**Authority:** Opportunity identity, scalp location, M5 executable timing, event freshness, late-entry protection, missed/re-arm rules and timing persistence.

## 1. Purpose

A valid market opportunity and a good executable scalp entry are different things.

This contract prevents two opposite errors:

- chasing a late Gold move because the thesis is attractive;
- deleting a valid Opportunity merely because the current M5 bar/timing is not ready.

## 2. Draft timeframe split

```text
H1  → broad regime / directional environment
M15 → opportunity location, path and structural context
M5  → primary executable setup/timing and fresh trigger
M1  → diagnostic micro-timing context only in baseline
quote/spread → current executable market condition
```

M1/tick authority remains a fresh-zero challenge item.

## 3. Opportunity lifecycle

Draft lifecycle:

```text
DISCOVERED
→ ARMED
→ WAITING / READY
→ TRIGGERED after governed broker lifecycle

ARMED / WAITING / READY
→ MISSED when a valid move becomes inefficient/late
→ INVALIDATED when thesis fails

MISSED
→ RE_ARMED only with explicit fresh event + surviving thesis
```

`STALE` may exist as vocabulary for a future generic expiry policy, but no automatic wall-clock expiry is implied until explicitly calibrated and frozen.

## 4. Opportunity identity

An Opportunity preserves:

- `opportunity_id`;
- market `episode_id`;
- BUY/SELL direction;
- lifecycle state;
- created/updated times;
- thesis/family attribution;
- structural source lineage;
- latest meaningful event time;
- timing result/reason;
- session/regime context;
- relevant cost/freshness observations.

A surviving same thesis keeps the same identity across WAIT/READY cycles and restart context.

A restored Opportunity is context only; fresh market intelligence and timing must revalidate it before action.

## 5. Terminal identity versus new episode

`MISSED`, `INVALIDATED` and any later approved `STALE` are terminal for that exact Opportunity identity.

Rules:

```text
same thesis still survives unchanged
→ do not fabricate a new ID

new/different thesis independently satisfies discovery
→ retire mismatched old plan
→ create new Opportunity + Episode IDs
```

`TRIGGERED` remains broker-lifecycle lineage until the managed trade is reconciled/closed.

## 6. Timing inputs

M5 timing may consume:

- M5 fine structure and sequence;
- latest causal structural/liquidity event;
- event age/freshness;
- M5 momentum/extension;
- M5 local location;
- M15 room/path;
- family-preferred trigger profile;
- session context;
- current spread/drift/cost context where available for analysis;
- optional M1 diagnostics if enabled.

No single optional primitive is required across every family.

## 7. Timing outcomes

```text
ENTER_BUY
ENTER_SELL
WAIT
MISSED
INVALID
```

`BLOCKED` belongs to Risk/Permissions/Execution.

### WAIT

Thesis survives, but current trigger/location/extension/freshness/cost efficiency is not acceptable yet.

### MISSED

The Opportunity was valid but the efficient entry window has passed. The system records it for counterfactual research and does not chase.

### INVALID

The underlying thesis/structure no longer survives.

### ENTER

The analytical trigger is currently ready. It still requires Trade Plan → Risk → hard authorities → Gate → Intent → broker write/reconciliation.

## 8. Event freshness

Scalping makes freshness a first-class timing concept.

Every structural/liquidity trigger used by timing must have an explicit causal knowledge timestamp. Timing may later classify it as:

```text
JUST_CONFIRMED
FRESH
AGING
STALE_FOR_ENTRY
```

Exact age thresholds can vary by event/family and remain calibration until challenged.

An event becoming stale for entry does not rewrite history or invalidate the original structural fact; it only means the current scalp should not be entered from that old event without fresh evidence.

## 9. Chase/extension protection

A move can be analytically correct but economically late.

Timing must distinguish:

- thesis strength;
- current extension;
- distance travelled since trigger;
- remaining structural target room;
- current transaction-cost burden;
- time since fresh event.

It must not improve apparent R by moving the stop or inventing a farther target.

## 10. Family-aware timing profiles

| Family | Draft M5 timing profile |
|---|---|
| Trend Pullback Continuation | pullback hold/reclaim + resumption |
| Breakout Expansion | accepted fresh break without chase |
| Breakout Retest Continuation | retest hold + continuation |
| Liquidity Sweep Reversal | sweep/reclaim + rejection/shift |
| Failed Breakout Reversal | failed acceptance + opposing response |
| Compression Expansion | fresh release + controlled follow-through |

Shared timing infrastructure may accept family parameters rather than duplicating six engines.

## 11. Re-arm / second chance

A MISSED Opportunity may re-arm only if:

- the underlying thesis still has relevance;
- a genuinely fresh causal event is proven;
- event timestamp differs meaningfully from the old trigger;
- current structural Trade Plan can be rebuilt;
- same-episode re-entry policy permits it;
- no unchanged next-poll signal is misrepresented as fresh evidence.

Automatic re-arm requires deterministic tests before production use.

## 12. Persistence ordering

Opportunity and Trade Plan lineage must remain consistent.

When a new episode replaces a terminal analytical opportunity:

```text
preserve old terminal event history
→ clear mismatched old Trade Plan
→ persist new Opportunity identity
→ build/save new Trade Plan only after later ENTER timing
```

This ordering prevents stale plan attachment after a crash.

## 13. Research classification

Research distinguishes:

- reconciled executed trades;
- WAITed opportunities;
- MISSED opportunities;
- INVALIDATED theses;
- hard-BLOCKED opportunities.

Counterfactual movement after a MISSED/BLOCKED setup is not actual P/L.

## 14. Dashboard

Show:

```text
Opportunity / Episode IDs
Direction + source families
Lifecycle state
Timing result + reason
latest fresh-event time / age
M5 momentum + extension
M15 room/location
cost/spread context
next authority
```

ENTER must never be displayed as “order sent” before broker reconciliation.

## 15. Planned implementation ownership

```text
src/gold_scalp_trader/decisions/opportunity.py
src/gold_scalp_trader/decisions/timing.py
src/gold_scalp_trader/decisions/snapshot.py
src/gold_scalp_trader/persistence/runtime_state.py
```

## 16. Planned proof

Tests must prove stable identity across WAIT, terminal identity semantics, fresh-event re-arm requirement, no unchanged-poll re-arm, restart context revalidation, event-age calculations, severe extension/chase WAIT/MISSED, plan lineage ordering and no broker authority.

## 17. Pre-challenge calibration

Open items: ARM/ENTER thresholds, family-specific event age, generic expiry versus event-based expiry, M1 role, distance-travelled chase logic, transaction-cost efficiency thresholds, re-arm definitions and same-episode re-entry limits.
