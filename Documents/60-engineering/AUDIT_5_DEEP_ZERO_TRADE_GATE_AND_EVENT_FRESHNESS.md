# GoldScalpTrader — Audit 5: Deep Zero-Trade, Gate and Event-Freshness Review

**Status:** FROZEN CORRECTIVE AUDIT PROTOCOL — NOT RUN
**Version:** 1.0-preservation-first-deep-zero-trade
**Authority:** Deep causal review of a low/zero-entry session across intelligence, strategies, Opportunity lifecycle, event freshness, TradePlan, monetary Risk and central Gate.

## 1. Why this audit exists

A geometry review can locate where candidates stopped but still miss stale upstream facts, incorrect Risk/profile state or misleading blocker presentation.

Traverse:

```text
MarketSnapshot
→ intelligence
→ six strategy families
→ BUY/SELL fusion + Red Team
→ Opportunity lifecycle
→ completed-M5 timing + event freshness
→ TradePlan gross/cost geometry
→ preserved monetary Risk profile/optional explicit aggressive overlay
→ session/news/system authorities
→ central Gate
→ Intent/precheck/writer/reconciliation
```

## 2. Freshness questions

For every Opportunity/Timing candidate identify thesis creation, latest causal event, knowledge time, M5 bars/minutes since event, distance travelled, extension, target room, spread/cost burden and whether re-arm had a genuinely new event.

No old BOS/MSS/sweep/retest may masquerade as current evidence.

## 3. Gate truth

Record independently:

```text
Gate reached? YES/NO
If NO: exact upstream owner/reason
If YES: Gate ALLOW/BLOCK/UNKNOWN + reason
Intent created? state
broker precheck reached?
writer send count
reconciliation state
```

`ENTRY_BLOCKED` label is not proof Gate ran.

## 4. Geometry freshness

Review live swing/zone lifecycle, breakout/retest relevance, exact sweep/failed-break freshness, consumed target/objective state, opposing structure, session/liquidity path and quote drift.

## 5. Transaction-cost review

Quantify where possible gross target, stop distance, current/historical healthy spread, slippage, cost-to-target/R, processing delay and actual minimum-lot monetary risk.

Separate analytical no-trade, TradePlan no-trade, Risk/account constraint and execution-friction no-trade.

## 6. Preserved Risk/session truth

Audit must use canonical policy rather than a generic or invented risk rule:

```text
SMALL / MEDIUM / NORMAL fixed risk-day profile
canonical profile bands
aggressive overlay disabled by default
8% max SL-risk ceiling (not target) only when explicitly enabled/eligible
16% aggregate/daily caps under that overlay
one fresh same-episode re-entry
three-loss / at-least-30-minute cooldown
1800s provider TTL
Daily PRE_CLOSE T-20/T-10
Weekend PRE_CLOSE T-60/T-30
Daily reopen 1 clean M5
Weekend reopen 2 clean M5 + gap assessment
```

If implementation differs without governed authorization, classify a preservation/document-code defect rather than “calibration too strict.”

## 7. Corrective categories

```text
MARKET_CONDITION_VALID_NO_TRADE
GENUINE_SCALP_CALIBRATION_TOO_STRICT
GENUINE_SCALP_CALIBRATION_TOO_LOOSE
STALE_EVENT_DEFECT
GEOMETRY_IMPLEMENTATION_DEFECT
FUSION/FAMILY_DEFECT
RISK_ACCOUNT_CONSTRAINT
PRESERVATION_VIOLATION
SESSION/NEWS_POLICY_EFFECT
PRESENTATION_ONLY_DEFECT
EXECUTION_LIFECYCLE_DEFECT
NO_DEFECT / MORE_EVIDENCE_NEEDED
```

## 8. Correction discipline

Never fix zero trades by bypassing Risk/Gate, inventing tight stops, reusing stale events or changing preserved non-scalp policy merely to increase frequency.

Every correction identifies classification, authoritative doc, source owner, regression tests and full affected graph.

## 9. Current state

```text
AUDIT RESULT: NOT RUN
No qualifying connected session has been reviewed yet.
```

Protocol is frozen; result remains NOT RUN.