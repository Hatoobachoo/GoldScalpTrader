# GoldScalpTrader — System Contract

**Status:** DRAFT PRE-CHALLENGE SYSTEM CONTRACT
**Version:** 0.1-system-invariants
**Authority:** Highest-level behavioural, chronology, ownership, accounting, recovery, learning and broker-safety invariants.

## 1. Purpose and conflict rule

This document is the constitution of GoldScalpTrader.

Every runtime mode, intelligence desk, strategy family, decision component, risk authority, broker operation, persistence workflow, learning path and operator view must preserve these invariants.

Topic contracts may add detail but must not silently contradict this file.

If a proposed change affects money, broker exposure, chronology, ownership, attribution, persistence, learning lineage, controller fencing or irreversible writes, implementation stops until the contradiction is resolved through `90-governance/DESIGN_DECISIONS.md` or `90-governance/OPEN_QUESTIONS.md`.

## 2. Whole lifecycle contract

```text
verified broker/provider facts
→ one immutable MarketSnapshot
→ independent bounded evidence
→ attributable scalp hypotheses
→ independent BUY / SELL theses
→ persistent Opportunity
→ fresh Entry Timing
→ structural Trade Plan
→ monetary RiskEvaluation
→ hard authorities
→ central ExecutionPermissionGate
→ durable one-shot ExecutionIntent
→ sole MT5Writer request
→ reconciliation against broker truth
→ managed trade lifecycle
→ verified close/accounting
→ durable downstream learning/research
```

No downstream component may retroactively invent upstream truth.

## 3. Truth and chronology invariants

1. Broker/account/symbol/quote/position/deal truth comes from the broker adapter boundary.
2. Candle-derived facts must record when they became knowable.
3. Forming candles cannot masquerade as completed-candle facts.
4. Derived structure, liquidity, FVG, order-block or other pattern evidence must preserve causal lineage.
5. Replay/research must use only information available at each simulated decision time.
6. Missing required truth remains UNKNOWN or BLOCKED; it is never guessed into PASS.
7. Restored local state is context, not broker truth.
8. Unknown exposure is never treated as zero.

The later scalp challenge may authorize carefully bounded forming-candle or tick-derived evidence, but such evidence must be explicitly typed and must never be mislabeled as completed-bar truth.

## 4. One-read-boundary invariant

A decision cycle begins from one normalized snapshot assembled through the MT5 read boundary.

Strategy families and analytical desks must not make hidden independent MT5 reads that produce inconsistent versions of market truth.

## 5. Parallel-analysis invariant

Parallelism is allowed only where dependencies permit and only for logically independent analytical work.

Valid examples:
- independent timeframe calculations from the same snapshot;
- independent structure/technical/liquidity computations after their declared dependencies;
- independent strategy-family evaluation;
- independent BUY and SELL thesis construction.

Parallel results must be deterministic in semantic meaning regardless of worker count.

## 6. Serial-authority invariant

Broker authority is strictly ordered.

```text
Trade Plan
→ Risk
→ session/news/system/account/controller authorities
→ central Gate
→ durable Intent
→ sole writer
→ reconciliation
```

No strategy, dashboard, learning process, research job or worker may bypass this chain.

## 7. Strategy/risk separation

Strategy decides whether a market thesis is worth pursuing.

Trade Plan defines entry reference, invalidation, objective hierarchy and structural geometry.

Risk decides whether the account can afford that already-defined geometry under broker constraints and policy.

Risk must never improve a setup by moving its structural stop merely to make lot sizing fit.

A high analytical score is not permission to exceed monetary risk limits.

## 8. Scalp-cost invariant

For scalping, executable cost is first-class truth.

The system must distinguish:
- chart/mid-price geometry;
- BUY entry at Ask / SELL entry at Bid;
- expected and actual spread;
- broker price precision and tick size;
- allowed deviation/slippage;
- executable stop/target distances;
- quote freshness.

A setup whose expected edge is consumed by spread/slippage must not be treated as equivalent to the same chart geometry under low-cost conditions.

## 9. Opportunity freshness invariant

A valid thesis and a valid current entry are different objects.

Opportunity identity, event lineage, trigger freshness and late-entry state must be durable and explicit.

The system must prevent:
- repeated recreation of the same already-terminal thesis;
- chasing an expired move;
- using stale BOS/MSS/sweep/retest evidence as a fresh trigger;
- duplicate entry from the same decision identity.

A genuinely new causal event may create a new opportunity under documented re-arm rules.

## 10. Risk invariants

At minimum, monetary risk architecture must support:

- account/symbol identity validation;
- broker minimum/maximum/step volume rules;
- stop-distance-aware sizing;
- margin/affordability checks;
- current exposure accounting;
- configurable per-trade risk ceilings;
- daily safety P/L and loss-lock state;
- consecutive-loss/cooldown state where adopted;
- one-position-at-a-time default unless a later explicit contract changes it;
- fail-closed handling when critical financial truth is missing.

No martingale or uncontrolled averaging is allowed.

## 11. Intent and execution invariants

Every irreversible broker action must have an identity.

For entry/modify/close actions:

1. the action must be authorized for its action type;
2. a durable Intent must exist before sending;
3. submission is one-shot unless reconciliation proves a safe, documented retry case;
4. the raw MT5 write boundary is singular;
5. timeout/uncertain acceptance becomes an explicit accepted-unknown/reconciliation state rather than blind resend;
6. broker response and subsequent broker truth must be reconciled;
7. duplicate submission is a safety defect.

## 12. Position-management invariant

Post-entry management does not create a new entry thesis.

The Trade Manager may return bounded management actions such as HOLD, PROTECT, TRAIL, RUNNER or EXIT only under its own documented contract.

Risk-reducing actions must remain action-sensitive; they must not inherit irrelevant entry-only vetoes without explicit rationale.

## 13. Accounting invariant

Bot-owned trading activity, manual/external activity and non-trading cash flow must remain distinguishable.

Daily account safety P/L must not be corrupted by deposits, withdrawals, credits or unrelated broker activity.

Bot performance statistics require verified lineage, not name/volume guesses.

## 14. Persistence and recovery invariants

Restart is not automatically a fresh trading day.

Durable state includes all obligations necessary to continue safely, including as applicable:
- risk-day state;
- active/pending Intent identity;
- Opportunity state;
- Trade Plan lineage;
- managed-trade context;
- close/reconciliation obligations;
- verified learning queues/receipts;
- policy/schema identity.

Startup must reconcile with current broker truth before granting new write authority.

## 15. Local backup invariants

Local backups are recovery artifacts, not trading authority.

- backup destination defaults outside the working repository;
- backup creation must not mutate broker state;
- backup failure is visible and classified;
- state snapshots must be internally consistent;
- a manifest/fingerprint should identify revision, schema/policy and included artifacts;
- `.env`, tokens, passwords and MT5 credentials are excluded from automatic archives;
- graceful shutdown may create a local state backup;
- graceful shutdown must not automatically push to GitHub.

## 16. Learning and AI invariants

Learning may observe, remember, research and propose.

Learning may not:
- relax hard monetary risk;
- change broker/account identity requirements;
- convert UNKNOWN into PASS;
- bypass session/news hard safety;
- send broker orders;
- self-promote a candidate into production policy.

Production policy changes require governed evidence and explicit promotion.

## 17. Dashboard invariant

Terminal and graphical dashboards are read-only presentation surfaces.

They consume authoritative DTO/state produced elsewhere. They do not own strategy, risk, lifecycle, controller or broker-write authority.

Presentation failure must not silently become trading permission or change broker state.

## 18. GitHub/runtime separation

The trading runtime does not require GitHub credentials.

No graceful-shutdown auto-push exists in the target design.

Repository publication is a controlled developer/operator action outside broker authority.

## 19. Evidence invariant

The project must distinguish:
- deterministic software proof;
- chronological replay/research evidence;
- connected read-only broker proof;
- connected DEMO lifecycle proof;
- calibration pending;
- external proof pending.

No green unit-test count may be described as proof of profitability or live execution readiness.
