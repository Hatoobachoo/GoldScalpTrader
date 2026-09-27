# GoldScalpTrader — Dashboard and UX Contract

**Status:** IMPLEMENTED OPERATOR UX — SWING-STYLE TERMINAL PRIMARY / GRAPHICAL SECONDARY  
**Version:** 4.0-swing-parity-scalp-floor  
**Authority:** Operator presentation hierarchy, bilingual/emoji visual language, fail-visible behavior, read-only controls, blocker/Gate truth, and dashboard liveness.

## 1. Constitutional hierarchy

GoldScalpTrader follows the completed GoldSwingTrader operator model:

```text
Authoritative runtime facts
        ↓
immutable DashboardData / normalized presentation projection
        ↓
PRIMARY: VS Code / terminal trading floor
        ↓ best-effort same facts
SECONDARY: localhost graphical/browser visual floor
```

The terminal is the primary operator surface. The browser is an optional read-only secondary projection. Closing or breaking the browser cannot stop the bot or hide the primary terminal floor.

Presentation owns zero broker, Risk, Gate, strategy-selection, Opportunity, promotion, or REAL-enable authority.

## 2. Implemented primary renderer stack

```text
terminal width 96+  → Rich institutional renderer
terminal width 64–95→ narrow stacked renderer
Rich/render failure → compact crash-safe fallback
```

All three retain the same authority truth. The primary floor is bilingual English/Urdu and uses emojis/status emphasis when available.

The normal wide hierarchy is:

```text
DOUBLE HEADER
Market • Session • Symbol • SELL • BUY
Spread • M5 Countdown • Action • News • Gate
M5 thesis • M1 subordinate timing • English/Urdu safety line

MARKET PICTURE                 TRADE SETUP
CURRENT DECISION / موجودہ فیصلہ
TRADE PLAN / تجارتی منصوبہ
STRATEGY ISOLATION • 1 ACTIVE + 5 SHADOW
RISK & ACCOUNT | TODAY / ACTIVITY | SYSTEM / EXECUTION
OPEN / MANAGED TRADE when present
LEARNING / DISCOVERY / BACKUP
```

The terminal frame is never reduced to a one-line status banner.

## 3. Always-visible rule

The operator floor remains meaningful when the system is:

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

> **UI fail-visible; trading fail-closed.**

Market CLOSED is a normal displayed state, not an application-exit instruction.

Missing authoritative facts render `UNKNOWN`, `—`, `WAIT`, `NOT EVALUATED`, or `NO SAMPLE`; presentation must never invent zero, plan geometry, Risk, performance, account facts, or broker state.

## 4. Market / setup / strategy-isolation truth

The dashboard reports market-first setup facts and then the current isolation policy:

```text
Detected Setup        actual market result
Active Family         exactly one ACTIVE_EXECUTION family
Shadow Board          five SHADOW_ONLY research families
Action                governed runtime result
```

A shadow setup is never displayed as a live broker trade. All-six research facts are visually separated from the one family permitted to originate live execution.

## 5. M5 / M1 timing presentation

```text
M5  primary setup / thesis / Opportunity
M1  subordinate entry refinement only after valid M5 Opportunity
M15 location/path context
H1  broad regime context
H4  major context
```

Presentation may show Opportunity identity/state, Timing READY/WAIT/MISSED/INVALID, timing profile, M5 event age, M1 trigger age, chase/micro-extension evidence and exact wait reason. M1 cannot independently create a production Opportunity.

## 6. Trade Plan / blocker / Gate

Only owned geometry may be shown:

```text
direction
entry reference
structural SL
primary target
expansion target
Gross R / target R where available
quality / invalidation source where available
```

No real plan → `WAITING` / `NOT AVAILABLE` / `—`.

Upstream stop and central Gate remain distinct. A dashboard refresh never evaluates a new Gate action.

## 7. Risk / account / execution

Where owned facts exist, show balance/equity/free margin, fixed risk profile, actual risk %, lot, position count/capacity, daily safety P/L, loss streak/cooldown, controller role, broker reconciliation, Intent/execution and management state.

Preserved monetary policy remains outside presentation:

| Profile | Normal | Elevated | Hard | Daily |
|---|---:|---:|---:|---:|
| SMALL | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

Aggressive mode stays disabled by default. The dashboard cannot change these values.

## 8. Learning / discovery presentation

Show actual timing/management learning, shadow evidence, discovery status and candidate/governance status only as research facts. Candidate stage never implies runtime activation.

Core invariant shown to the operator:

> **The bot may learn how to trade better; it may not learn how to bypass its safety system.**

## 9. Implemented secondary graphical floor

`DASHBOARD_MODE=GUI` adds the browser **in addition to** the terminal primary.

The secondary visual floor uses the GoldSwing institutional visual language adapted to Scalp:

- dark navy/black + cyan/gold framing;
- robot masthead;
- Arabic invocation plus English/Urdu operator text;
- market/session/live-price/countdown/status strip;
- M1/M5/M15/H1/H4 completed-candle chart tabs;
- Indicators / Drawings / Bars local visual controls;
- Market Analysis / Trend / Session-News / Timing panels;
- Current Signal / Decision;
- Trade Plan;
- current blocker/Gate;
- 1 ACTIVE + 5 SHADOW strategy board;
- Risk/account;
- Open/Managed Trade;
- Activity/Learning/Discovery/Execution/System floor;
- explicit stale/offline overlay.

The browser has **no BUY/SELL/MODIFY/CLOSE controls** and no state-changing HTTP endpoint.

## 10. Presentation cadence and failure semantics

A fast presentation refresh may update already-owned quote/clock/countdown/cached facts. It must not rerun strategy selection, Opportunity, Risk, Gate, or broker execution merely because the screen refreshed.

```text
secondary browser fails
→ primary terminal remains alive
→ trading authority unchanged

runtime/MT5 cycle fails
→ primary shows DEGRADED / exact reason
→ no broker action from failed cycle
→ safe polling may continue

market CLOSED
→ full primary and secondary floors remain visible
```

## 11. Final invariant

> **GoldScalpTrader has one primary terminal trading floor and, when enabled, one secondary localhost read-only visual floor. Both present the same normalized authority facts with Swing-style hierarchy, emojis and English/Urdu cues. Presentation can reveal authority; it can never create it.**
