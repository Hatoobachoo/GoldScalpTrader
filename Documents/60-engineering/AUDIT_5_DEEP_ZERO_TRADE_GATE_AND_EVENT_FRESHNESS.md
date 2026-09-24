# GoldScalpTrader — Audit 5: Deep Zero-Trade, Gate and Event-Freshness Review

**Status:** DRAFT CORRECTIVE AUDIT PROTOCOL — NOT RUN
**Version:** 0.1-scalp-deep-zero-trade
**Authority:** Deep causal review of a low/zero-entry session across intelligence, strategies, Opportunity lifecycle, event freshness, TradePlan, monetary Risk and central Gate.

## 1. Why this audit exists

A geometry review can show where candidates stopped but still miss upstream stale facts or misleading blocker presentation.

This audit traverses the complete entry chain:

```text
MarketSnapshot
→ intelligence / structure / technical / liquidity / quant / session
→ strategy families
→ BUY/SELL fusion + Red Team
→ Opportunity lifecycle
→ entry timing + event freshness
→ TradePlan geometry
→ monetary Risk
→ session/news/system authorities
→ central Gate
→ Intent/precheck/writer/reconciliation
```

## 2. Freshness questions

For every candidate reaching Opportunity/Timing identify:

- thesis creation time;
- latest causal supporting event time;
- confirmation/knowledge time;
- M5 bars/minutes since event;
- distance travelled since event;
- current extension;
- current target room;
- current spread/cost burden;
- whether the family had a genuinely fresh re-arm event.

No old BOS/MSS/sweep/retest may masquerade as current evidence.

## 3. Gate truth

Record separately:

```text
Gate reached? YES/NO
If NO: exact upstream stopping stage/reason
If YES: Gate PASS/BLOCK/UNKNOWN + reason
Intent created? state
broker precheck reached?
writer send count
reconciliation state
```

A runtime `ENTRY_BLOCKED` label is not proof Gate evaluated.

## 4. Geometry freshness

Review whether levels used by TradePlan remain causally live:

- swing/zone still active;
- breakout/retest boundary still relevant;
- sweep/failed-break event exact and fresh;
- target not already consumed;
- new opposing structure not ignored;
- session/liquidity path not stale;
- quote drift has not invalidated approved geometry.

## 5. Transaction-cost review

Because this is a scalper, quantify where possible:

- gross target distance;
- stop distance;
- current/historical healthy spread;
- expected/observed slippage;
- cost-to-target and cost-to-R ratio;
- processing/submit delay;
- minimum-lot monetary risk.

Separate analytical no-trade from execution-cost no-trade.

## 6. Corrective categories

```text
MARKET_CONDITION_VALID_NO_TRADE
CALIBRATION_TOO_STRICT
CALIBRATION_TOO_LOOSE
STALE_EVENT_DEFECT
GEOMETRY_IMPLEMENTATION_DEFECT
FUSION/FAMILY_DEFECT
RISK_ACCOUNT_CONSTRAINT
SESSION/NEWS_POLICY_EFFECT
PRESENTATION_ONLY_DEFECT
EXECUTION_LIFECYCLE_DEFECT
NO_DEFECT / MORE EVIDENCE NEEDED
```

## 7. Correction discipline

Never fix “zero trades” by bypassing Risk/Gate, inventing tight stops, reusing stale events or lowering policy without evidence.

Every correction identifies authoritative doc, source owner, focused tests and affected graph.

## 8. Current state

```text
AUDIT RESULT: NOT RUN
No qualifying connected session has been reviewed yet.
```
