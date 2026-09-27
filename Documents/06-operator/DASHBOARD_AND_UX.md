# GoldScalpTrader — Dashboard and UX Contract

**Status:** IMPLEMENTED OPERATOR UX — SWING-STYLE TERMINAL PRIMARY / GRAPHICAL SECONDARY  
**Version:** 4.1-swing-parity-roman-urdu-scalp-floor  
**Authority:** Operator presentation hierarchy, English + Roman Urdu visual language, fail-visible behavior, read-only controls, blocker/Gate truth, and dashboard liveness.

## 1. Constitutional hierarchy

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

Presentation owns zero broker, Risk, Gate, strategy-routing, Opportunity, promotion, or REAL-enable authority.

## 2. Language contract

Operational dashboard language is **English + Roman Urdu**, matching normal conversational usage:

```text
WAIT  | Intazar
BUY   | Kharid
SELL  | Farokht
WHY   | Wajah
Current Decision | Maujooda Faisla
Trade Plan       | Mansuba
Risk & Account   | Risk aur Account
Open Trade       | Khula Trade
System           | Nizam
Learning         | Seekhna
Discovery        | Daryaft
```

Urdu script is not used for operational labels/status/reasons. The Arabic invocation may remain as a decorative masthead element because it is not an authority-bearing operator control.

## 3. Primary renderer stack

```text
terminal width 96+   → Rich institutional renderer
terminal width 64–95 → narrow stacked renderer
Rich/render failure  → compact crash-safe fallback
```

All three retain the same authority truth and Roman Urdu cues.

The wide hierarchy is:

```text
IDENTITY HEADER
GoldScalpTraderAI • PRIMARY LIVE SCALPING FLOOR
M5 thesis • M1 timing • structural routing • governed execution

MARKET STRIP
Market • Soft Context • Symbol • SELL • BUY • Spread • M5 Countdown • Action • Gate

MARKET PICTURE                 TRADE SETUP / ROUTE
CURRENT DECISION / Maujooda Faisla
TRADE PLAN / Mansuba
STRATEGY / SETUP BOARD • 1 Routed + 5 Shadow
RISK & ACCOUNT | TODAY / ACTIVITY | SYSTEM / EXECUTION
OPEN / MANAGED TRADE when present
LEARNING / DISCOVERY
```

The identity header and live market strip are deliberately separate so the top of the primary floor does not become visually cramped.

## 4. Always-visible rule

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

Market CLOSED is a displayed runtime state, not an application-exit instruction. Missing facts remain `UNKNOWN`, `—`, `WAIT`, `NOT EVALUATED`, or `NO SAMPLE`; presentation never invents zero, plan geometry, Risk, performance, account facts, or broker state.

## 5. Session truth in presentation

Hard broker Session and soft/contextual session labels must not be conflated.

```text
Hard Session  → OPEN / PRE_CLOSE / CLOSED / UNKNOWN authority
Soft Context  → NEW_YORK / LONDON overlap / contextual label only
Schedule      → VERIFIED / UNVERIFIED
News          → contextual/soft health
```

A header must never show `Session NEW_YORK` in a way that can be mistaken for hard Session OPEN when hard Session is actually UNKNOWN.

## 6. Market / setup / routed-family truth

The dashboard reports market-first setup facts and current production routing:

```text
Detected Setup        actual market result
Routed Family         exactly one ACTIVE_EXECUTION family when structurally resolved
Shadow Board          remaining research families
Action                governed runtime result
```

Production routing is structural, not highest-score selection and not manual `ACTIVE_STRATEGY_FAMILY` selection. Opposite qualified directions produce WAIT/no routed family.

A shadow setup is never displayed as a live broker trade. All-six research facts are visually separated from the one structurally routed production family.

## 7. M5 / M1 timing presentation

```text
M5  primary setup / thesis / Opportunity
M1  subordinate entry refinement only after valid M5 Opportunity
M15 location/path context
H1  broad regime context
H4  major context
```

Presentation may show Opportunity identity/state, Timing READY/WAIT/MISSED/INVALID, profile, M5 event age, chase/micro-extension evidence and exact wait reason. M1 cannot independently create a production Opportunity.

## 8. Trade Plan / blocker / Gate

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

Upstream stop and central Gate remain distinct. Dashboard refresh never evaluates a new Gate action.

## 9. Risk / account / execution

Where owned facts exist, show balance/equity/free margin, fixed risk profile, actual risk %, lot, position count/capacity, daily safety P/L, loss streak/cooldown, controller role, broker reconciliation, Intent/execution and management state.

Preserved monetary policy remains outside presentation:

| Profile | Normal | Elevated | Hard | Daily |
|---|---:|---:|---:|---:|
| SMALL | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

Aggressive mode stays disabled by default. The dashboard cannot change these values.

## 10. Secondary graphical floor

`DASHBOARD_MODE=GUI` adds the browser **in addition to** the terminal primary.

The browser uses the Swing institutional floor composition adapted to Scalp:

- robot/title masthead, invocation, Roman Urdu discipline line, clock and mode;
- symbol / hard market state / **Soft Context** / live price / spread / M5 countdown / bot status strip;
- left rail: Market Analysis, Trend Direction, Session/News, Timing Intelligence;
- center: completed-candle M1/M5/M15/H1/H4 chart with local visual controls;
- right rail: Current Signal/Decision, Trade Plan, blocker/Gate, Multi-Timeframe/Setup;
- bottom row: Risk & Account, one Strategy/Setup Board, Open/Managed Trade;
- lower row: Execution & Controller, Trading Activity, Learning & Discovery, System & Data, Recent Verified Closes, discipline tile;
- explicit stale/offline overlay.

The Strategy board appears once in the lower floor; the right rail is reserved for multi-timeframe/setup context rather than duplicating the same board.

The browser has **no BUY/SELL/MODIFY/CLOSE controls**, no broker endpoint, and no state-changing HTTP method.

## 11. Presentation controls

M1/M5/M15/H1/H4, Indicators, Drawings, Settings and Bars are local presentation state only. They cannot change strategy cadence, family routing, Opportunity, Risk, Gate, Intent or MT5 state.

## 12. Presentation cadence and failure semantics

A fast presentation refresh may update already-owned quote/clock/countdown/cached facts. It must not rerun family routing, Opportunity, Risk, Gate, or broker execution because the screen refreshed.

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

## 13. Final invariant

> **GoldScalpTrader has one primary terminal floor and one optional secondary localhost read-only visual floor. Both show the same normalized authority facts using Swing-style hierarchy, emojis and English + Roman Urdu cues. Presentation can reveal authority; it can never create it.**
