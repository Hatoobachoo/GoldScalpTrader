# GoldScalpTrader — User Manual

**Status:** POST-AUDIT-1 USER GUIDE — IMPLEMENTATION PENDING
**Version:** 1.0-fresh-zero-user
**Authority:** Human-facing intended operation and interpretation; topic contracts own trading behaviour.

## 1. What the bot is intended to do

GoldScalpTrader is a local Exness MT5 XAUUSD/XAUUSDm system for selective short-duration Gold scalps. It is a governed multi-desk system, not a simple EMA cross bot and not HFT.

Current architecture is frozen after Fresh-Zero Audit 1, but final runtime/broker-write implementation is not yet claimed complete.

## 2. Frozen trading personality

```text
H1   broad soft regime
M15  opportunity/location/path
M5   primary completed-bar setup/timing/management
H4   optional major context
M1   diagnostic/research only
quote current executable Bid/Ask/spread/drift/health
```

It prefers fresh, cost-aware, clearly invalidatable scalps and refuses late/stale/cost-dominated setups.

## 3. Intended future workflow

1. Open MT5/connect intended account/server.
2. Start READINESS/DRY_RUN first.
3. Verify account/symbol/data/recovery truth.
4. Read Current Blocker and Gate separately.
5. Let governed analysis/management run.
6. Use controlled DEMO PRIMARY only after that implementation milestone is proven.
7. Stop with governed shutdown; local runtime checkpoint occurs after broker/controller authority is safely released.

REAL mode is not a V1 shortcut.

## 4. Decision path

```text
MarketSnapshot
→ Intelligence
→ six strategy families
→ BUY/SELL + Red Team
→ persistent Opportunity
→ completed-M5 Entry Timing
→ TradePlan gross + cost-adjusted room
→ STANDARD monetary Risk
→ Session/News/account/exposure/controller
→ central Gate
→ one-shot Intent
→ sole writer
→ broker reconciliation
```

A candidate can stop before Gate; `ENTRY_BLOCKED` does not automatically mean Gate BLOCKED.

## 5. Six strategy families

1. Trend Pullback Continuation
2. Breakout Expansion
3. Breakout Retest Continuation
4. Liquidity Sweep Reversal
5. Failed Breakout Reversal
6. Compression Expansion

All six do not need to agree. Correlated evidence from the same event is not counted repeatedly as independent confirmation.

## 6. Opportunity / freshness

A strong idea can wait for efficient entry. Outcomes include WAIT, ENTER, MISSED and INVALID. Terminal setup does not reset on next poll; re-arm needs a genuinely fresh causal event.

M1 cannot independently create a V1 production entry.

## 7. TradePlan / costs

TradePlan creates structural Entry Reference, invalidation/SL, Primary/optional Expansion/exceptional Runner objectives and original R before money sizing.

It also retains current known cost-adjusted room. Swing's old 1.20R floor is not automatically used; exact scalp thresholds remain calibration pending.

Structural stop is never tightened just to make minimum lot fit.

## 8. Risk / small account

V1 uses one `STANDARD` production Risk policy, not automatic SMALL/MEDIUM/NORMAL balance tiers.

If theoretical lot is below broker minimum:

```text
evaluate actual broker minimum volume
→ calculate actual risk at structural stop
→ PASS only inside hard STANDARD policy
→ otherwise BLOCK current TradePlan
```

Current 0.50% scaffold is provisional. Historical 8%/16% aggressive values are not active V1 policy. Any future aggressive experiment is explicit and disabled by default.

No martingale, grid rescue or averaging down. One independent Gold risk position per scope.

## 9. Session / News

For new entry:

```text
OPEN + CLEAR    → may proceed
OPEN + BLACKOUT → BLOCK
OPEN + UNKNOWN  → BLOCK / LIMITED
```

UNKNOWN is never shown as CLEAR. Existing-position protection/mandatory CLOSE remains action-sensitive.

## 10. Management

```text
HOLD | PROTECT | TRAIL | RUNNER | EXIT
```

Time/efficiency failure is an EXIT reason so a failed scalp does not quietly become a swing. Runner is exceptional and needs fresh continuation/new objective.

## 11. Manual/external trades

Unknown manual/foreign Gold exposure is never adopted and can block new entry. A human close of an already-known bot ManagedTrade can complete lifecycle only after exact broker proof, with close-origin attribution preserved.

## 12. Multi-laptop rule

Different independent account/symbol scopes may run separately. Same-scope simultaneous PRIMARY writers are unsupported. Same-scope movement is sequential stop/checkpoint/transfer/restore/reconcile/controller acquisition.

## 13. Runtime local backup

No automatic GitHub push on shutdown.

```text
transactional local state
→ rolling runtime checkpoint
→ final graceful-shutdown local checkpoint
→ optional portable runtime recovery package
```

Secrets are excluded.

## 14. Development/source backup

After a **major coherent bulk**, one pull is enough:

```powershell
git pull --ff-only
```

Your local clone then contains the latest project and full Git history. Optionally create a secret-clean Windows ZIP after important milestones for another offline copy. No need to pull after every tiny patch.

## 15. DRY_RUN meaning

DRY_RUN may exercise market→decision→TradePlan→Risk→Gate diagnostics but sends no irreversible broker order and cannot prove fills/slippage/reconciliation/profitability.

## 16. Troubleshooting

If waiting, read Current Blocker, Gate separately, human explanation and health/logs. Do not weaken safety merely to force a trade, delete state to reset locks or run a same-scope second writer.

## 17. Current proof boundary

Architecture Audit 1 is complete. Final package/runtime/tests/DEMO execution/learning/local recovery are still implementation or external evidence work. No profitability claim exists.