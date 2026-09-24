# GoldScalpTrader — User Manual

**Status:** POST-AUDIT-1 USER GUIDE — PRESERVATION-FIRST CORRECTED / IMPLEMENTATION PENDING
**Version:** 1.2-preserved-risk-features-user
**Authority:** Human-facing intended operation and interpretation; topic contracts own trading behaviour.

## 1. What the bot is intended to do

GoldScalpTrader is a local Exness MT5 XAUUSD/XAUUSDm system for selective short-duration Gold scalps. It is a governed multi-desk system, not a simple EMA cross bot and not HFT.

GoldSwingTraderAI remains the default feature/default baseline. Only direct scalp-specific differences or explicit operator-directed changes are allowed before final documentation review.

## 2. Scalp trading personality

```text
H1   broad soft regime
M15  opportunity/location/path
M5   primary completed-bar setup/timing/management
H4   optional major context
M1   diagnostic/research only
quote current executable Bid/Ask/spread/drift/health
```

The system prefers fresh, cost-aware, clearly invalidatable scalps and refuses late/stale/cost-dominated entries.

## 3. Decision path

```text
MarketSnapshot
→ bounded-parallel Intelligence
→ six strategy families
→ BUY/SELL + Red Team
→ persistent Opportunity
→ completed-M5 Entry Timing
→ TradePlan gross + cost-adjusted room
→ SMALL/MEDIUM/NORMAL monetary Risk
   + optional explicit aggressive overlay
→ Session/News/account/exposure/controller
→ central Gate
→ one-shot Intent
→ sole writer
→ broker reconciliation
```

A candidate can stop before Gate; `ENTRY_BLOCKED` does not automatically mean Gate BLOCKED.

## 4. Six strategy families

1. Trend Pullback Continuation
2. Breakout Expansion
3. Breakout Retest Continuation
4. Liquidity Sweep Reversal
5. Failed Breakout Reversal
6. Compression Expansion

These reference families are preserved. Correlated evidence from one event is not repeatedly counted as independent certainty.

## 5. Opportunity / freshness

A strong idea can WAIT for an efficient entry. Terminal setup does not reset merely on the next poll; re-arm needs genuinely fresh causal evidence.

M1 cannot independently create a production entry.

## 6. TradePlan / costs

TradePlan creates structural Entry Reference, invalidation/SL, Primary/optional Expansion/Runner objectives and original R before money sizing.

Scalp adds explicit cost-adjusted room and stronger entry-drift/freshness checks.

Swing's 1.20R floor is not automatically used as the hard scalp entry floor; exact scalp target-quality thresholds remain evidence questions.

Structural stop is never tightened to make minimum lot fit.

## 7. Preserved account Risk profiles

```text
SMALL   positive DayStartEquity < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

| Profile | Normal / target | Elevated | Hard ceiling | Daily loss lock |
|---|---:|---:|---:|---:|
| SMALL | 3.0%–4.5% | >4.5%–6.5% | 7% | 12% |
| MEDIUM | 2.0%–3.0% | >3.0%–4.5% | 5% | 9% |
| NORMAL | 1.0%–2.0% | >2.0%–3.5% | 4% | 7% |

Profile is fixed from DayStartEquity for the UTC risk day.

If theoretical lot is below broker minimum:

```text
evaluate actual broker minimum volume
→ calculate actual risk at structural stop
→ PASS only if active policy permits
→ otherwise BLOCK current TradePlan
```

## 8. Aggressive small-account mode

This feature is **preserved** and **disabled by default**.

When explicitly enabled for eligible sub-$1,000 operation:

```text
8%  = MAXIMUM monetary SL-risk ceiling per trade
      NOT a target
16% = maximum aggregate open risk
16% = daily loss ceiling
```

It never automatically enables merely because the account is small. All normal structural, session, News, exposure, controller, Gate and execution safeguards remain active.

## 9. Daily lock / reset / cooldown

Manual daily-loss reset capability is preserved but disabled by default.

Preserved baseline:

- one genuinely fresh same-episode re-entry can be allowed;
- if it also loses, that episode locks;
- three consecutive closed bot losses trigger at least 30 minutes global cooldown;
- fresh/healthy release conditions must also pass.

Restart does not clear these states.

## 10. Session / News and API failure

For new entry:

```text
OPEN + current News CLEAR    → may proceed
OPEN + current News BLACKOUT → BLOCK
OPEN + true NEWS_UNKNOWN     → BLOCK / LIMITED
```

Temporary provider/API error:

```text
refresh fails + still-valid last-known-good cache
→ use cached accepted calendar
→ provider may show DEGRADED

refresh fails + expired/invalid/no cache
→ NEWS_SAFETY_UNKNOWN
→ new entry blocked
```

The bot never rewrites an old cache timestamp/TTL just to keep trading.

Preserved baselines:

```text
Provider TTL 1800 seconds
Daily T-20 no entry / T-10 flatten
Weekend T-60 no entry / T-30 flatten
Daily reopen 1 clean completed M5
Weekend reopen 2 clean completed M5 + gap assessment
```

Current broker schedule still needs connected verification.

## 11. Management

```text
HOLD | PROTECT | TRAIL | RUNNER | EXIT
```

Scalp-specific differences:

- time/efficiency failure can cause EXIT;
- Runner is exceptional and needs fresh continuation/new objective.

Optional partial management remains supported where current volume is broker-valid/divisible. A 0.01 position is not required to partial-close for the system to work correctly.

## 12. Manual/external trades

Unknown manual/foreign Gold exposure is never adopted and can block new entry. A human close of a known bot ManagedTrade can complete lifecycle only after exact broker proof with correct close-origin attribution.

## 13. Bounded analytical concurrency

Independent desks/families retain bounded-parallel execution as a planned feature. A deterministic one-worker fallback must produce semantically identical outputs.

Money/broker authority stays serial.

## 14. Runtime capability stages

```text
READINESS
DRY_RUN
controlled DEMO PRIMARY
future governed REAL
```

REAL is preserved as a future capability but cannot be enabled until its separate DEMO/release/explicit-approval gate is satisfied.

## 15. Runtime local backup

No automatic GitHub push on shutdown.

```text
transactional local state
→ rolling runtime checkpoint
→ final graceful-shutdown local checkpoint
→ optional portable runtime recovery package
```

## 16. Development/source backup

After a major coherent bulk:

```powershell
git pull --ff-only
```

One pull updates the local clone and full Git history. Optional secret-clean ZIP can provide another offline copy.

## 17. Exact Swing → Scalp differences

Read:

`Documents/90-governance/DOCUMENTATION_COMPARISON.md`

It now records:

- genuine scalp-specific changes;
- explicit operator-directed changes;
- preserved Swing features/defaults;
- earlier unintended removals that have been restored.

## 18. Current proof boundary

Documentation is still in freeze preparation. Final package/runtime/tests/DEMO execution/learning/local recovery/current broker proof are not yet claimed complete. No profitability claim exists.

Before implementation, the remaining genuinely scalp-specific differences will be discussed with the operator during final documentation review.