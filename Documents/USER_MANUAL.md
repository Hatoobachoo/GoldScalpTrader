# GoldScalpTrader — User Manual

**Status:** DRAFT PRE-CHALLENGE USER GUIDE — IMPLEMENTATION PENDING
**Version:** 0.1-scalp-local-recovery
**Authority:** Human-facing operation and interpretation. Trading behaviour remains owned by canonical topic contracts.

## 1. What this bot is intended to do

GoldScalpTrader is being designed as an Exness MT5 XAUUSD/XAUUSDm system for selective short-duration Gold scalps.

It is not a simple EMA cross bot and it is not intended to chase every small move. It uses a governed multi-desk process: trustworthy market facts, market intelligence, independent strategy families, BUY/SELL debate, persistent Opportunity, entry timing, structural TradePlan, monetary Risk, hard safety, one-shot execution and broker reconciliation.

The current project is still in documentation/challenge stage. Broker-write operation is not yet claimed implemented.

## 2. Draft trading personality

Current pre-challenge baseline:

```text
H1   broad regime/context
M15  opportunity/location/path
M5   primary scalp setup/timing/management
H4   optional major context
M1   diagnostic baseline; challenge may change it
```

Exact roles are not frozen until the fresh-zero architecture review completes.

The bot is intended to prefer **fresh, executable, cost-aware** setups rather than old signals, late chases or structurally attractive trades whose spread/slippage/minimum lot makes them uneconomic.

## 3. Normal future daily workflow

Once the documented runtime is implemented:

1. Open MT5 and connect the intended account/server.
2. Confirm intended Gold symbol.
3. Start READINESS or DRY_RUN first.
4. Wait for startup/recovery/identity/data truth.
5. Read **Current Blocker** and **Gate** separately.
6. Leave the process running for governed analysis/management.
7. Use PRIMARY/DEMO broker writes only after that milestone is explicitly implemented and certified.
8. Stop with governed shutdown/Ctrl+C.
9. Successful shutdown releases broker/controller authority first, then creates a verified **local** runtime checkpoint/backup.

Never delete runtime state or edit SQLite to reset risk/learning history.

## 4. DRY_RUN meaning

DRY_RUN is not fake live trading.

It can exercise:

```text
market facts
→ intelligence
→ strategies/fusion
→ Opportunity/timing
→ TradePlan
→ Risk
→ hard permission/Gate diagnostics
```

but it cannot send a real broker order.

A DRY_RUN “BUY READY” means analytical/risk conditions reached that state. It does not prove a broker fill, slippage, reconciliation or profitability.

## 5. Dashboard time and sizing

Human-facing time may use Pakistan Standard Time (PKT, UTC+05:00). Internal market/risk/persistence/research timestamps remain UTC.

Intended primary terminal sizing:

```text
64–95 display cells → narrow stacked view
96+ display cells    → wide Rich view
```

Presentation width does not change trading logic.

## 6. Session and News

Session and News are separate truths.

The bot may show:

```text
Soft Session  ASIA / LONDON / NEW YORK / OVERLAP / OFF HOURS
Hard Market   OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN
News          CLEAR / BLACKOUT / UNKNOWN / POST-NEWS WARMUP
```

Known high-impact blackout is a hard new-entry condition in the current draft.

Missing News is never shown as CLEAR.

The final treatment of `Market OPEN + News UNKNOWN` is still a pre-build design decision for this scalping project; the User Manual will be updated after Audit 1 freezes it.

## 7. Feed health is not trade readiness

Fresh price means the feed/process is alive. It does not mean a trade is permitted.

Possible reasons for waiting include:

- insufficient/stale/sparse/corrupt data;
- no valid strategy edge;
- Opportunity exists but timing is WAIT;
- event is stale/entry would be chased;
- TradePlan geometry is poor;
- minimum 0.01 lot is unaffordable at the structural stop;
- session/news/risk/controller/reconciliation blocks;
- spread/drift/trigger freshness is unacceptable.

The dashboard remains visible during normal WAIT states.

## 8. Entry path

Intended future broker-capable path:

```text
Fresh safe market facts
→ Intelligence + strategy families
→ BUY / SELL + Red Team
→ Opportunity
→ Entry Timing
→ structural TradePlan
→ independent monetary Risk
→ Session/News/account/exposure/controller authorities
→ central Execution Gate
→ durable one-shot Intent
→ sole MT5Writer
→ broker reconciliation
```

A setup can stop at TradePlan or Risk **before** the central Gate is evaluated.

## 9. Current Blocker versus Gate

This is essential when asking “why no trade?”

Example — upstream stop:

```text
Analytical BUY READY
TradePlan DEGRADED
Current Blocker TradePlan
Gate NOT EVALUATED / WAIT
```

This is **not** a central Gate rejection.

Example — actual Gate block:

```text
TradePlan READY
Risk PASS
Current Blocker Execution Gate
Gate BLOCKED
Reason <actual hard authority>
```

A broad `ENTRY_BLOCKED` action is not automatically `Gate BLOCKED`.

## 10. Strategy floor

Starting draft has six independent families:

1. Trend Pullback Continuation
2. Breakout Expansion
3. Breakout Retest Continuation
4. Liquidity Sweep Reversal
5. Failed Breakout Reversal
6. Compression Expansion

All six do not need to agree. BUY and SELL cases remain independent. Optional Fib/FVG/Order Block/Trendline/POC context cannot become hidden universal filters.

The fresh-zero review may keep, merge, split, replace or remove families before implementation freeze.

## 11. Opportunity and entry freshness

A good market thesis can wait for a better entry.

The system distinguishes:

```text
Opportunity exists
Timing WAIT
Timing ENTER
MISSED — efficient window passed
INVALID — thesis failed
```

A MISSED/terminal setup does not simply reset on the next poll. Re-arm requires a genuinely fresh causal event.

Scalp-specific focus includes event age, movement since event, extension, remaining room, spread and drift.

## 12. TradePlan

TradePlan creates structural geometry before money sizing:

```text
approved entry reference
structural invalidation / SL
Immediate obstacle
Primary scalp objective
optional Expansion
exceptional Runner objective where justified
original R
cost/room context
```

The final minimum structural R/cost-adjusted target policy is still under challenge/calibration. Swing's 1.20R value is not automatically the scalp rule.

A structural stop is never tightened just to make 0.01 lot affordable.

## 13. Risk and small account

Risk is independent from strategy score.

The bot is being designed specifically to handle small-account broker granularity correctly:

```text
theoretical lot below 0.01
→ evaluate actual broker minimum 0.01
→ calculate real all-in risk for structural stop
→ PASS only if final policy allows it
→ otherwise BLOCK current TradePlan
```

Exact profile percentages/daily-loss limits are not frozen yet. Current old scaffold 0.50% is provisional. Reference aggressive Swing percentages are not automatically copied.

Hard principles already remain:

- no martingale;
- no uncontrolled grid;
- no averaging-down rescue;
- one independently risk-bearing Gold position per scope in initial V1;
- manual daily-loss reset disabled by default;
- unknown financial truth is not zero.

## 14. Targets and management

Intended management actions:

```text
HOLD | PROTECT | TRAIL | RUNNER | EXIT
```

For a scalper, time/efficiency also matters. A position should not quietly turn into an accidental swing merely because SL has not been touched.

Exact time-stop/protection/Primary/Expansion/Runner policies remain calibration items.

Original R remains immutable for learning even after stop protection.

## 15. Manual trades

Manual/foreign Gold positions are not silently adopted.

| Manual activity | Intended bot response |
|---|---|
| manual Gold position while bot flat | external exposure shown; new bot entry may be blocked |
| external/manual realized deal | kept separate from bot performance |
| human closes exact known bot ManagedTrade | exact broker history can finish bot lifecycle with EXTERNAL/MIXED close origin |
| partial/ambiguous close | remain RECONCILING |

Bot trade counts refer to verified bot entry lineages, not signals or manual trades.

## 16. Multi-laptop rule

Allowed:

```text
Laptop A → Account A → PRIMARY
Laptop B → Account B → PRIMARY
```

Not supported in V1:

```text
Laptop A → Account A → PRIMARY
Laptop B → same Account A → second active writer
```

Same-scope movement is sequential: stop old PRIMARY, create/verify local recovery package, restore new DB, reconnect/reconcile broker truth, then acquire new controller authority.

## 17. Learning

Future verified DEMO trades can create downstream learning only after exact broker closure evidence.

The learning flow preserves family, policy version, Entry Reference, actual fill, original R, ticket/Opportunity/TradePlan lineage and causal post-entry path.

Learning can research/propose. It cannot change hard Risk, bypass Gate or directly send orders.

## 18. Local backup

GoldScalpTrader intentionally does **not** push to GitHub automatically on shutdown.

Local durability layers:

```text
local project clone + .git history
rolling runtime checkpoints
final graceful-shutdown local checkpoint
portable local recovery package
optional local Git bundle at deliberate source milestone
optional second physical drive copy
```

Conceptual backup root:

```text
C:\GoldScalpTrader_Backups\
```

Real `.env`, passwords, tokens, broker credentials and private keys are excluded from automatic recovery packages.

## 19. Graceful shutdown

Future operator output should truthfully resemble:

```text
🛑 Closing GoldScalpTrader safely...
✅ New work stopped
✅ Trading/controller authority released
💾 Creating final verified local checkpoint...
🔐 Integrity/secret scan passed
✅ Local backup created: <id/path>
✅ Closed safely
```

If backup fails, it must say so. It must not print fake success.

There is no shutdown Git commit/push step.

## 20. Restore / machine migration

A backup is context, not current broker truth.

Restore flow:

```text
verify manifest/hashes/secrets
→ restore NEW DB/path
→ configure machine credentials separately
→ connect intended MT5 account/server/symbol
→ read current positions/deals/quote
→ reconcile Intents/ManagedTrade/Risk/Learning
→ acquire controller
→ READY only after all hard authorities pass
```

Never restore by overwriting a live active DB in place.

## 21. Learning/research evidence

Research distinguishes:

- actual verified trades;
- MISSED opportunities;
- hard-BLOCKED opportunities;
- capacity-suppressed setups;
- broker/system faults.

Backtests/shadow outcomes are not actual broker P/L.

Scalp research emphasizes net expectancy after costs, MAE/MFE, entry/capture efficiency, spread/slippage, latency, duration and min-lot affordability—not win rate alone.

## 22. Troubleshooting rule

If the bot is waiting:

1. read Current Blocker;
2. read Gate separately;
3. read the human explanation;
4. inspect health/logs if needed;
5. do not weaken safety merely to generate a trade.

Do not delete state, modify DB locks manually, run same-scope second PRIMARY, commit credentials or switch to a future REAL mode casually.

## 23. Current proof boundary

Today the project is still a **DRAFT PRE-CHALLENGE documentation design** plus provisional DRY_RUN scaffold.

Do not interpret this manual as proof that final runtime, broker execution, learning, dashboard or local recovery tooling is already implemented.

After all documents are complete, Audit 1 will challenge the design from zero before implementation starts.