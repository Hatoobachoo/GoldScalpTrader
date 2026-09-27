# GoldScalpTrader — Dashboard and UX Contract

**Status:** APPROVED OPERATOR UX ARCHITECTURE — TERMINAL PRIMARY / GRAPHICAL SECONDARY
**Version:** 3.0-terminal-primary-scalp-floor
**Authority:** Operator presentation hierarchy, fail-visible behavior, read-only controls, blocker/Gate truth, and dashboard liveness.

## 1. Constitutional hierarchy

GoldScalpTrader follows the completed GoldSwingTrader operator architecture:

```text
Authoritative runtime facts
        ↓
immutable DashboardData / presentation projection
        ↓
PRIMARY: VS Code / terminal dashboard
        ↓ best-effort same facts
SECONDARY: localhost graphical/browser dashboard
```

The terminal dashboard is the normal operator surface. The graphical dashboard is optional, local-only, read-only, and secondary. Closing or breaking the browser must not stop the bot or remove the primary dashboard.

Presentation has zero broker, Risk, Gate, strategy-selection, Opportunity, or REAL-enable authority.

## 2. Always-visible rule

The primary dashboard remains visible when the system is:

```text
OPEN
PRE_CLOSE
CLOSED
UNKNOWN
WAITING
NO VALID SETUP
DEGRADED
MT5 initialize/login failure
quote/feed failure
Session/provider ambiguity
reconciliation wait
runtime exception
DEMO confirmation/safety block
```

The presentation rule is:

> **UI fail-visible; trading fail-closed.**

A market-closed state is a normal operator state, not a reason to hide or terminate the dashboard.

If authoritative facts are unavailable, render `UNKNOWN`, `—`, `WAIT`, `NOT EVALUATED`, or `NO SAMPLE`; never fabricate zeroes, candles, Risk, plan geometry, or performance.

## 3. Primary terminal floor

The terminal renderer is width-aware:

- 64–95 columns: stacked narrow frame;
- 96+ columns: denser two-column institutional frame;
- rendering failure must degrade to truthful text, not grant authority or terminate trading.

The primary frame must show, as available:

```text
GoldScalpTrader identity / bot health
Market state / soft Session / symbol
Bid / Ask / spread
Detected setup
ACTIVE_EXECUTION family
live action / exact reason
central Gate truth
Opportunity / Timing / M1 refinement evidence
TradePlan
Risk
ManagedTrade
execution / Intent / management activity
shadow-family observations
learning/governance status
News context (soft only)
system/data health
```

The terminal frame is not a one-line status banner.

## 4. Detected setup and strategy isolation

The dashboard reports what the market actually produced. It must not force the configured active family onto every market episode.

```text
active family has valid own setup → may progress through governed pipeline
shadow family has setup → show SHADOW ONLY; cannot originate live trade
no valid setup → WAIT / NO VALID SETUP
```

All six families must never appear as if they are blended into one production trade.

## 5. M5 / M1 timing presentation

Canonical Scalp roles remain:

```text
M5  primary setup / thesis / Opportunity
M1  subordinate entry refinement only after valid M5 Opportunity
M15 location/path context
H1  broad regime context
H4  optional major context
```

M1 cannot independently create a production trade.

Preferred timing facts:

```text
Opportunity state / ID / episode
Timing READY / WAIT / MISSED / INVALID
M5 event age
M1 trigger age / profile
entry-ready reason
```

## 6. Trade Plan / blocker / Gate truth

Show only actual governed geometry:

```text
direction
approved entry reference
current executable quote when available
structural SL
primary target
expansion target
Gross R
cost/quality evidence when available
```

No real plan = `NOT AVAILABLE` / `—`.

Upstream blocker and central Gate are distinct:

```text
Setup Detector block     → Gate NOT EVALUATED
Entry Timing block       → Gate NOT EVALUATED
TradePlan block          → Gate NOT EVALUATED
Executable Quality block → Gate NOT EVALUATED
Risk block               → Gate NOT EVALUATED
actual central Gate block→ Gate BLOCKED
```

## 7. Risk and account display

Presentation must preserve the configured Risk truth without inventing values. Reference bands remain:

| Profile | Normal | Elevated | Hard | Daily |
|---|---:|---:|---:|---:|
| SMALL | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

Where authoritative facts exist, show balance/equity/free margin, proposed lot/risk, position capacity, daily P/L/loss budget, loss streak/cooldown, re-entry state, aggressive-mode state, and manual-reset state.

Aggressive mode remains disabled by default. If explicitly enabled, 8% is a maximum single-trade SL-risk ceiling, not a target; 16% aggregate/day limits remain governed outside presentation.

## 8. ManagedTrade / execution / learning

When flat, show `NONE`. When open, show authoritative ManagedTrade lineage and current management facts only.

Actual broker execution, shadow research, replay, counterfactual results, and candidate research must remain visually distinguishable.

Learning panel may show:

```text
actual timing/management evidence
shadow evidence
counterfactual research
candidate stage
APPROVAL_REQUIRED
```

It must never imply a research candidate already owns live authority.

## 9. Secondary graphical dashboard

The localhost browser dashboard remains useful and is retained as a secondary visual floor.

Requirements:

- bind to `127.0.0.1` only;
- consume atomic read-only snapshots;
- no broker-mutating endpoint;
- no BUY/SELL/CLOSE/MODIFY authority;
- browser failure never stops trading or the primary terminal dashboard;
- stale/missing snapshot renders truthful offline/stale state;
- M1/M5/M15/H1/H4 chart tabs are presentation-only;
- Indicators / Drawings / Settings are local visual controls only;
- no-scroll institutional layout remains the graphical target.

`DASHBOARD_MODE=GUI` means **enable the secondary browser in addition to the primary terminal dashboard**. It does not replace the primary operator/runtime path.

## 10. Presentation cadence

A fast presentation refresh may update already-owned facts such as clock, Bid/Ask/spread, quote age, countdown, and cached system/account state. It must not rerun strategies, mutate Opportunity, rebuild Risk/Gate, or create broker actions merely because the screen refreshed.

## 11. Failure semantics

```text
secondary browser fails
→ primary terminal remains alive
→ trading/runtime authority unchanged

runtime/MT5 cycle fails
→ primary terminal shows DEGRADED / exact reason
→ no broker action from failed cycle
→ polling may continue for recovery

market CLOSED
→ full dashboard remains visible
→ action WAIT / blocked as owned by runtime facts
```

## 12. Final invariant

> **GoldScalpTrader always has a primary terminal trading floor. The optional graphical dashboard is a secondary read-only projection. Market closure, feed faults, MT5 faults or runtime problems must become visible dashboard states—not reasons for the operator surface to disappear.**
