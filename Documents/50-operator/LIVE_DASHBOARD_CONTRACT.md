# GoldScalpTrader — Live Dashboard Contract

**Status:** FROZEN V1 CANONICAL EXTENSION — PRESERVATION-FIRST CORRECTED / IMPLEMENTATION PROOF PENDING
**Version:** 1.0-profiled-risk-cache-aware-live-ux
**Authority:** Primary terminal presentation, nominal read-only liveness, authoritative session/News/provider/Risk visibility, verified strategy-performance visibility, terminal-width behaviour and presentation crash isolation.

## 1. Relationship to main dashboard contract

This document extends `DASHBOARD_AND_UX.md` and creates no trading authority.

The dashboard consumes already-owned facts from runtime, market data, intelligence, strategy, TradePlan, Risk, execution, learning and persistence/local-backup modules.

## 2. Intended implementation owners

```text
operator/presentation.py      read-only blocker/Gate normalization and wording
operator/narrow_dashboard.py  stacked primary renderer
operator/rich_dashboard.py    wide primary renderer
operator/compact_dashboard.py dependency-light fallback
operator/live_dashboard.py    shared DTO/helpers/emoji vocabulary
operator/__init__.py          width dispatcher + optional graphical publication
app/live_presentation.py      quote/account/provider/profile enrichment
app/loop.py                   presentation pulse separate from trading cadence
```

Terminal is primary operational dashboard. Browser dashboard is secondary/read-only.

## 3. Width and fallback

```text
64–95 display cells → narrow stacked renderer
96+ cells           → wide Rich renderer
Rich/render failure → compact fallback
```

Presentation failure cannot terminate trading or create permission.

## 4. Timing rule

```text
Presentation pulse: nominal fast read-only refresh
Trading decision: governed completed-M5/event cadence
```

The pulse may update PKT clock, live Bid/Ask, spread, M5 countdown, quote age, provider/cache age and already-owned account facts.

It may not rerun strategy families, create Opportunity, rebuild TradePlan, change Risk profile/overlay, change Gate, create Intent or call broker writes.

## 5. Session / News display

Show already-computed:

```text
Soft Session
Hard Market State
News State
Provider Health
Provider Source LIVE / FILE / LKG CACHE
cache age / valid-until
next event / countdown
```

Current new-entry semantics are frozen:

```text
OPEN + accepted CLEAR    → may proceed to other authorities
OPEN + BLACKOUT          → BLOCK
OPEN + true UNKNOWN      → BLOCK / LIMITED
```

A temporary refresh error does not itself mean UNKNOWN when a still-valid accepted LKG cache exists. UNKNOWN is never rendered CLEAR; expired cache is never rendered current.

Preserved baseline facts/policy inputs shown only when owned/authoritative:

```text
Provider TTL 1800s
Daily PRE_CLOSE T-20 / T-10
Weekend PRE_CLOSE T-60 / T-30
Daily reopen 1 clean M5
Weekend reopen 2 clean M5 + gap assessment
```

## 6. Terminal hierarchy

Wide-screen conceptual hierarchy:

```text
HEADER
  product / stage / PKT / Market / Session / News / Gate
  XAU SELL / BUY / spread / quote age / M5 countdown / Today P&L

NEWS / PROVIDER
  source / health / cache age-validity / next event

MARKET PICTURE
  H1 / M15 / M5 / optional H4 / diagnostic M1

CURRENT DECISION
  BUY / SELL / leading family / Red Team / Opportunity / Timing / WHY

TRADE PLAN
  Approved Entry Reference / current quote / SL / objectives
  gross room / cost-adjusted room / freshness

RISK & ACCOUNT
  SMALL/MEDIUM/NORMAL profile
  normal/elevated/hard/daily values
  actual proposal
  aggressive mode DISABLED/ENABLED
  if enabled: 8% MAX SL-risk ceiling — NOT TARGET; 16% aggregate/daily ceilings
  reset / streak / cooldown / capacity

OPEN TRADE / ACTIVITY / SYSTEM / EXECUTION / LEARNING / LOCAL BACKUP
```

Narrow layout preserves meaning in stacked form.

## 7. Strategy visibility

All six production families remain active internally. Primary screen may prioritize leading BUY/SELL thesis, Opportunity, Timing, coverage, correlation, Red-Team conflict and concise reason rather than display noisy full rows continuously.

## 8. Verified strategy performance

Only exactly-once verified actual closed ManagedTrades in the approved environment count as production performance.

```text
signal != trade
blocked entry != trade
open position != closed sample
replay/shadow != actual production performance
zero samples → NO SAMPLE
```

## 9. Current decision / blocker / Gate truth

```text
TradePlan stop before Gate
→ blocker TradePlan
→ Gate NOT EVALUATED

Risk/profile/overlay rejection before Gate
→ blocker Risk
→ Gate NOT EVALUATED

session/news owner blocks upstream
→ show owning blocker
→ do not fabricate Gate BLOCKED

actual central Gate BLOCK
→ blocker Execution Gate
→ Gate BLOCKED
```

## 10. Trade setup truth

Display only actual governed TradePlan geometry. No plan means no fabricated Entry/SL/targets/R.

No dashboard sentence hard-codes Swing 1.20R as the scalp floor. Show the actual versioned TradePlan reason/policy.

## 11. Scalp-specific live facts

Where authoritative, show event/trigger age, M5 freshness, Approved Entry Reference vs current quote, spread, cost-adjusted room, latency diagnostics, Opportunity re-arm state and open-trade age/bars.

## 12. Risk/account presentation

Do not collapse Risk to one `STANDARD` label.

Show active profile and actual reference profile bands. Show aggressive overlay separately and truthfully. If disabled, say disabled. If enabled, explicitly label 8% as a **maximum ceiling, not target**.

No RiskEvaluation → `Risk Standby`, not false failure.

## 13. Open Trade

Show verified direction/ticket, actual Entry, current price, original/current SL, objectives, original/current R/open risk, remaining volume, any verified partial management, trade age/bars, Trade Manager action/reason and Intent/reconciliation/close state.

Time/efficiency is a normal EXIT reason. Dashboard never grants MODIFY/CLOSE authority.

## 14. Runtime capability display

Display capability stage truthfully:

```text
READINESS
DRY_RUN
DEMO PRIMARY
REAL — FUTURE/GATED, not enabled merely by UI selection
```

REAL remains a preserved future capability but requires its own release/approval gate.

## 15. Secondary graphical boundary

Graphical dashboard consumes a read-only atomic snapshot with identical blocker/Gate/profile/provider meanings. Browser failure must not affect PRIMARY.

## 16. Planned proof

Tests cover width/fallback, live pulse without new decision, cache/provider provenance, profile/aggressive-mode rendering, 8%-ceiling wording, blocker-vs-Gate truth, no-plan geometry, verified performance, PKT/M5 countdown, read-only authority, partial-state rendering and graphical snapshot consistency.