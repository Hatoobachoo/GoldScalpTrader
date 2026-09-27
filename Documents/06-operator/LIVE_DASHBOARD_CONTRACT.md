# GoldScalpTrader — Live Dashboard Contract

**Status:** APPROVED — PRIMARY TERMINAL LIVE DASHBOARD / SECONDARY GRAPHICAL PROJECTION
**Version:** 3.0-live-presentation
**Authority:** Live presentation cadence, dashboard liveness, failure visibility, and authority separation.

## 1. Primary surface

The terminal dashboard is the primary live operator surface. It is expected to stay present throughout the runtime lifecycle, including non-trading and degraded states.

The graphical/browser dashboard is a secondary local projection only.

## 2. Liveness contract

The dashboard must remain visible through:

```text
startup/readiness
market OPEN
market PRE_CLOSE
market CLOSED
Session UNKNOWN
no valid setup
Timing WAIT/MISSED
TradePlan unavailable
Risk/Gate block
reconciliation wait
MT5/data/provider fault
runtime exception
secondary graphical failure
```

Market closure is not an application-exit signal.

## 3. Fail-visible / fail-closed rule

```text
presentation should fail visible
trading should fail closed
```

A failed runtime cycle must not produce an unverified broker write. The primary dashboard should show the exact problem and continue polling where safe so transient faults can recover.

If startup/configuration cannot proceed, render a complete terminal safety/error frame before exit rather than only a traceback or silent termination.

## 4. Runtime versus presentation cadence

Dashboard refresh does not create decision authority.

A presentation refresh may update facts already owned by runtime/data sources, such as:

- current clock;
- Bid/Ask/spread;
- quote age;
- countdown;
- cached account/system facts;
- latest completed decision/plan/management state.

It may not independently rerun strategy selection, create Opportunity, change Risk, evaluate Gate for a new action, or call broker-write code.

## 5. Primary terminal content

At minimum the primary frame must expose:

```text
bot/system health
market state / session
symbol / Bid / Ask / spread
setup / active family / action / reason
Opportunity / Timing evidence
TradePlan
Risk
Gate/blocker truth
ManagedTrade
execution/Intent/management state
shadow observations
learning/governance status
News context
```

Narrow terminals use a stacked layout; wider terminals may use a denser multi-column layout.

## 6. Secondary browser content

The browser may add richer chart and visual controls but must represent the same authority truth.

If browser publication/server fails:

```text
primary terminal continues
runtime continues according to its own authorities
browser failure is shown in System health when possible
no trading permission changes
```

## 7. `DASHBOARD_MODE`

```text
TERMINAL → primary terminal only
GUI      → primary terminal + optional secondary localhost graphical dashboard
```

`GUI` does not replace the primary runtime or terminal surface.

## 8. Runtime fault examples

### MT5 unavailable

```text
Bot Status    DEGRADED
Action        WAIT
Market        UNKNOWN
Reason        MT5 initialize/login/read error
Execution     NO BROKER ACTION FROM FAILED CYCLE
System        DASHBOARD ALIVE • TRADING FAIL-CLOSED
```

### Market closed

```text
Market        CLOSED
Action        WAIT / runtime-owned state
Dashboard     fully visible
```

### Secondary browser unavailable

```text
Primary       ACTIVE
Graphical     SECONDARY UNAVAILABLE
Trading       unaffected by presentation failure
```

## 9. No fabricated truth

Missing values must remain missing/unknown. Never convert unavailable account/Risk/plan/performance facts into zero for prettier presentation.

## 10. Final invariant

> **The operator should always be able to see what the bot knows, what it does not know, why it is waiting or blocked, and whether any presentation subsystem is degraded. The dashboard must never disappear merely because the market is closed or another subsystem has a problem.**
