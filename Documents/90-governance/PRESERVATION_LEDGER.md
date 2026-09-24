# GoldScalpTrader — Documentation Preservation Ledger

**Status:** DRAFT PRESERVATION LEDGER — PRE-CHALLENGE
**Version:** 0.1-reference-meaning-preservation
**Authority:** Proof that useful GoldSwingTraderAI design meaning is preserved, adapted or explicitly excluded in GoldScalpTrader canonical `Documents/`.

## 1. Purpose

GoldScalpTrader is intentionally derived from the architecture/governance system of GoldSwingTraderAI while changing trading personality to scalping.

Preservation means:

```text
preserve useful rationale / authority boundaries
adapt trading-timeframe/geometry/risk semantics for scalping
explicitly remove irrelevant/undesired reference behaviour
keep current truth reconstructable from GoldScalpTrader Documents/
```

It does **not** mean copying every numerical threshold or historical implementation result.

## 2. Major preservation map

| Reference subject | GoldScalpTrader canonical destination | Preservation/adaptation |
|---|---|---|
| product vision / non-goals | `00-foundation/PROJECT_VISION.md` | swing personality replaced by scalp personality |
| system invariants | `00-foundation/SYSTEM_CONTRACT.md` | safety/chronology/lifecycle preserved |
| staged parallel + serial authority | `ARCHITECTURE.md`, `TRADING_FLOOR_ARCHITECTURE.md` | preserved |
| build dependency order | `BUILD_PHASES.md` | preserved/adapted to docs-first challenge |
| MT5 read boundary/history | `10-market-intelligence/MARKET_DATA_AND_HISTORY.md` | preserved + stronger freshness/cost context |
| candle/structure | `CANDLE_STRUCTURE.md` | preserved causal knowledge time |
| technical/liquidity/indicators/session/news | corresponding `10-*` docs | preserved; scalp freshness/path emphasis |
| six-family floor | `20-trading-decisions/STRATEGY_FLOOR.md` | starting decomposition preserved, challengeable |
| BUY/SELL fusion | `SCORING_AND_DECISION_FUSION.md` | preserved |
| Opportunity/timing | `ENTRY_TIMING.md` | preserved + stronger event freshness/chase handling |
| structural TradePlan | `TRADE_PLAN.md` | preserved; R/target policy recalibrated |
| breakout/reversal geometry extensions | two geometry docs | preserved/adapted to scalp M5 event boundaries |
| Trade Manager | `TRADE_MANAGER_AND_EXIT.md` | preserved + time/efficiency scalp exit |
| monetary risk | `RISK_CONTRACT.md` | architecture preserved; reference percentages not frozen |
| manual/broker activity | `BROKER_ACTIVITY_AND_MANUAL_TRADES.md` | preserved |
| session/news/risk state | `SESSION_AND_RISK_STATE_MACHINE.md` | preserved; News UNKNOWN policy reopened |
| provider contract | `SESSION_NEWS_PROVIDER_CONTRACT.md` | preserved |
| one-shot execution/reconciliation | `EXECUTION_AND_BROKER_SAFETY.md` | preserved + scalp friction/latency |
| persistence/recovery | `PERSISTENCE_RESTART_AND_RECOVERY.md` | preserved; remote auto-push removed |
| learning/research/discovery/promotion | all `40-*` docs | preserved + scalp cost/duration evidence |
| operator dashboards | all `50-*` docs | preserved + scalp facts |
| coding/testing/audits | all `60-*` docs | preserved; audits truthful NOT RUN initially |
| governance | all `90-*` docs | preserved/adapted |

## 3. Explicitly not inherited as frozen truth

The following reference details are deliberately **not** copied as final scalp truth before challenge/evidence:

- swing-oriented H4/H1/M15/M5 hierarchy exactly as-is;
- M1 diagnostic-only as immutable rule;
- 1.20R Primary target floor;
- aggressive SMALL-account risk percentages;
- exact daily-loss/cooldown thresholds;
- `OPEN + News UNKNOWN → PASS` as automatic scalp policy;
- exact pre-close/reopen timings;
- default runner behaviour;
- historical zero-trade audit findings;
- reference source/test PASS claims.

These are DRAFT/CALIBRATE/EXTERNAL items in GoldScalpTrader.

## 4. Explicitly removed reference behaviour

### Runtime graceful-shutdown Git publication

GoldSwingTraderAI's runtime automatic Git commit/push/archive publication is **not** part of GoldScalpTrader.

Replacement:

```text
rolling local StateStore/checkpoints
+ final verified local graceful-shutdown checkpoint
+ deliberate portable recovery package
+ optional deliberate local source Git bundle
```

Trading runtime has no Git credential/push authority.

## 5. New/stronger scalp emphasis

GoldScalpTrader strengthens or adds first-class design treatment for:

- trigger/event freshness;
- target-room transaction-cost context;
- spread/slippage/drift/processing latency;
- short-horizon hold/time efficiency;
- min-lot affordability separation from strategy quality;
- cost-aware replay/stress;
- failed-scap-to-accidental-swing prevention;
- local independent backup/recovery.

## 6. Historical/reference evidence boundary

GoldSwingTraderAI audits/results are design lessons, not GoldScalpTrader evidence.

A reference defect may motivate a preventive contract/test, but GoldScalpTrader audits remain `NOT RUN` until its own source/runtime evidence exists.

## 7. Freeze requirement

Before implementation freeze, `AUDIT_1_FRESH_DESIGN_REVIEW.md` must challenge every preserved/adapted item and record KEEP/CHANGE/REMOVE/ADD/CALIBRATE/EXTERNAL verdicts.

This ledger then updates to reflect final accepted preservation decisions.
