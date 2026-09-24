# GoldScalpTrader — System Contract

**Status:** FROZEN V1 SYSTEM CONTRACT — CALIBRATION / EXTERNAL PROOF PENDING
**Version:** 1.0-post-fresh-zero-invariants
**Authority:** Highest-level behavioural, chronology, ownership, accounting, recovery, learning and broker-safety invariants.

## 1. Constitution / conflict rule

Every runtime mode, intelligence desk, strategy family, decision component, Risk authority, broker operation, persistence workflow, learning path and operator view preserves this contract.

Topic contracts add detail but cannot silently contradict it. A change affecting money, broker exposure, chronology, ownership, persistence, learning lineage, controller fencing or irreversible writes stops implementation until the canonical graph is reconciled through active Design Decisions/Open Questions.

## 2. Whole lifecycle

```text
verified broker/provider facts
→ one immutable MarketSnapshot
→ causal independent evidence
→ six attributable scalp hypotheses
→ independent BUY / SELL theses + Red Team
→ persistent Opportunity
→ completed-M5 Entry Timing / event freshness
→ structural TradePlan + gross/cost-adjusted room
→ STANDARD monetary RiskEvaluation
→ hard authorities
→ central ExecutionPermissionGate
→ durable one-shot ExecutionIntent
→ sole MT5Writer
→ broker reconciliation
→ ManagedTrade / Trade Manager
→ verified close/accounting
→ durable downstream learning/research
```

No downstream component may retroactively invent upstream truth.

## 3. Frozen timeframe / chronology invariants

```text
H1   broad soft regime
M15  opportunity/location/path
M5   primary completed-bar setup/timing/management
H4   optional major context
M1   diagnostic/research only
quote current executable condition only
```

- candle-derived production facts use completed bars and causal knowledge time;
- forming candles cannot masquerade as completed facts;
- M1/tick-history cannot silently become production trigger authority in V1;
- current quote/tick may invalidate executability but not fabricate historical structure;
- replay uses only information available at simulated decision time;
- UNKNOWN required truth is never guessed into PASS/CLEAR/zero;
- restored local state is context, not broker truth;
- unknown exposure is never zero.

## 4. One-read-boundary invariant

A governed cycle begins from one normalized snapshot assembled through the MT5 read boundary. Analytical desks/families do not make hidden independent MT5 reads.

## 5. Logical parallel / physical concurrency invariant

Specialist/family work is logically independent where dependencies allow. Physical concurrent workers are optional/profiling-driven.

Any concurrent implementation must use immutable inputs, deterministic canonical output order, no lifecycle side effects and semantic parity with a one-worker path.

## 6. Serial authority invariant

```text
TradePlan
→ STANDARD Risk
→ session/news/system/account/controller authorities
→ central Gate
→ durable Intent
→ fresh broker checks
→ sole writer
→ reconciliation
```

No strategy, dashboard, research, learning or analytical worker bypasses this chain.

## 7. Strategy / geometry / Risk separation

Strategy chooses whether thesis is worth pursuing. Entry Timing decides current M5 readiness. TradePlan defines structural entry/invalidation/objectives and gross/cost-adjusted room. STANDARD Risk decides monetary affordability for that already-defined geometry.

Risk never moves structural stop or increases because analytical confidence is high.

## 8. Cost invariant

Scalping distinguishes Signal Price, Approved Entry Reference, executable Bid/Ask, Actual Fill, structural stop/target, spread, explicit reserves and actual slippage/fees.

Costs are counted exactly once. A setup whose remaining edge is consumed by friction is not equivalent to the same chart geometry under low costs.

## 9. Opportunity freshness invariant

Opportunity identity, causal event lineage, trigger age and late-entry state are explicit/durable.

Prevent repeated recreation of terminal thesis, stale BOS/MSS/sweep/retest entry, late chase and duplicate entry from same decision identity. Re-arm requires a genuinely new causal event.

## 10. Risk invariants

- one V1 `STANDARD` production risk policy;
- broker min/max/step and actual normalized-volume risk;
- structural-stop-aware sizing;
- margin/affordability/exposure checks;
- preferred target + hard per-trade ceiling + daily safety limit;
- durable loss/cooldown/re-entry state;
- one independent Gold risk position per scope;
- manual daily-loss reset disabled by default;
- fail closed on missing critical financial truth;
- no martingale, uncontrolled grid or averaging-down rescue;
- historical aggressive 8%/16% values are not active policy.

Exact numeric values remain calibration pending.

## 11. News/session invariant

For V1 new entry:

```text
OPEN + NEWS_CLEAR    → may proceed
OPEN + NEWS_BLACKOUT → BLOCK
OPEN + NEWS_UNKNOWN  → BLOCK / LIMITED
```

UNKNOWN is never renamed CLEAR. Existing-position management/protection/mandatory CLOSE remains action-sensitive.

## 12. Intent / execution invariants

Every irreversible broker action has durable identity before send. One Intent has at most one irreversible send allowance. MT5 raw write boundary is singular. Timeout/uncertain acknowledgement becomes reconciliation, never blind resend. Local lifecycle changes only from broker-verified truth.

READINESS/DRY_RUN precede any writer. Controlled DEMO is first broker-write target; REAL is outside V1 without separate governance.

## 13. Position-management invariant

Trade Manager owns only:

```text
HOLD / PROTECT / TRAIL / RUNNER / EXIT
```

Time/efficiency failure is an EXIT reason, not a separate V1 action. Risk-reducing CLOSE remains action-sensitive and does not mechanically inherit every OPEN friction veto.

## 14. Accounting / ownership

Bot-owned activity, external/manual activity and non-trading cash flow remain distinguishable. Bot performance requires verified lineage. Unknown external positions are never silently adopted.

## 15. Persistence / recovery

Restart is not a fresh day. Durable state preserves risk-day, Opportunity/TradePlan, Intent, ManagedTrade, close/reconciliation, learning queue/receipt and policy/schema identity as applicable.

Startup reconciles current broker truth before write authority. Current broker truth outranks restored local context.

## 16. Runtime local backup

Runtime checkpoints/recovery packages are local recovery artifacts, not broker authority. Backup root is outside repo by default; secrets are excluded; consistent snapshots are required; failure is explicit.

Graceful shutdown may create a verified local checkpoint but performs no Git commit/push/pull.

## 17. Development/source backup

Normal low-usage workflow:

```text
one coherent remote commit
→ operator git pull --ff-only
→ local clone contains latest source + full Git history
→ optional secret-clean ZIP milestone copy
```

Git bundle is optional advanced/manual tooling only.

## 18. Learning / research / AI

Learning may observe, remember, research and propose. It cannot relax hard Risk, bypass identity/session/news/controller/reconciliation, call writer or self-promote production policy.

Production changes require governed evidence/promotion.

## 19. Dashboard invariant

Terminal/browser dashboards consume authoritative state and are read-only. Presentation failure never creates permission or broker-state mutation.

## 20. Evidence invariant

Keep separate frozen design, calibration pending, deterministic software proof, chronological replay evidence, connected read-only proof, connected DEMO lifecycle proof, local recovery proof and external proof.

No test count proves profitability or future live performance.