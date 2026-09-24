# GoldScalpTrader — Canonical Documentation Manual

**Status:** AUDIT 1 COMPLETE — PRESERVATION-FIRST CORRECTION / FREEZE PREPARATION
**Version:** 1.2-preservation-first
**Authority:** Entry point, reading order, document ownership and design-before-code boundary.

## 1. What this manual is

`Documents/` is the sole current design, implementation and verification authority for GoldScalpTrader.

GoldScalpTrader is the scalping-specialized sibling of GoldSwingTraderAI. The reference project's feature set, engineering boundaries, safety model, learning/recovery system and governance remain the default baseline.

The governing preservation rule is:

> **Keep the GoldSwingTraderAI feature/default unless a direct scalping requirement, an explicit operator instruction, or a separately proven reference defect justifies changing it.**

A simpler implementation is not, by itself, permission to remove an inherited feature.

If it is unclear whether a proposed difference is genuinely scalp-specific, preserve the reference behaviour now and discuss the possible change during final documentation review.

## 2. Project method

```text
complete canonical draft manual
→ Fresh-Zero Audit 1                         COMPLETE
→ preservation-first correction              CURRENT / core decisions corrected
→ synchronize complete affected graph
→ metadata/cross-link Documentation Audit
→ final operator discussion of true scalp deltas
→ freeze accepted architecture contracts
→ implement from contracts
→ verify Documents → Code → Tests/Evidence
→ connected DEMO/recovery proof
→ future governed REAL only after its own gate
```

Code must not outrun the canonical manual.

## 3. Canonical inventory

Reference-equivalent inventory remains:

```text
Top level                  7
00-foundation              5
10-market-intelligence     7
20-trading-decisions       7
30-risk-execution          6
40-research-learning       7
50-operator                3
60-engineering            14
90-governance              8
TOTAL                      64
```

## 4. Canonical reading order

1. `README.md` + `GLOSSARY.md`;
2. `00-foundation/PROJECT_VISION.md`;
3. `00-foundation/SYSTEM_CONTRACT.md`;
4. `00-foundation/ARCHITECTURE.md`;
5. `00-foundation/TRADING_FLOOR_ARCHITECTURE.md`;
6. `00-foundation/BUILD_PHASES.md`;
7. all `10-market-intelligence/` contracts;
8. all `20-trading-decisions/` contracts;
9. all `30-risk-execution/` contracts;
10. all `40-research-learning/` contracts;
11. all `50-operator/` contracts;
12. `60-engineering/*`;
13. all `90-governance/` files;
14. `CODER_GUIDE.md`;
15. `PROJECT_BUILD_AND_RECOVERY_GUIDE.md`;
16. `SETUP_AND_RUN_GUIDE.md`;
17. `USER_MANUAL.md`;
18. `FINAL_BUILD_PROMPT.md`.

Conflict order:

```text
SYSTEM_CONTRACT
→ owning topic contract
→ active DESIGN_DECISIONS
→ OPEN_QUESTIONS / preserved-default register
→ Architecture / Trading Floor
→ engineering/operator summaries
```

## 5. Preserved architectural spine

```text
one MT5 read boundary
→ immutable MarketSnapshot
→ causal market intelligence
→ bounded-parallel independent analytical desks/families
→ six independent strategy-family hypotheses
→ independent BUY / SELL fusion + Red Team
→ persistent Opportunity
→ completed-M5 Entry Timing + event freshness
→ family-aware structural TradePlan
→ gross + cost-adjusted room truth
→ profiled monetary Risk (SMALL / MEDIUM / NORMAL)
   + optional explicit disabled-by-default aggressive small-account overlay
→ hard session/news/system/account/controller authorities
→ central ExecutionPermissionGate
→ durable one-shot ExecutionIntent
→ sole MT5Writer
→ reconciliation against broker truth
→ ManagedTrade / Trade Manager
→ verified close
→ durable learning/research evidence
→ local backup/recovery
```

Financial/broker authority remains serial even when analytical work is bounded-parallel.

## 6. Scalp-specific timeframe roles

```text
H1   broad soft regime / major directional-volatility context
M15  opportunity location, path, liquidity/session context
M5   primary completed-bar setup, entry timing and normal management
H4   optional major context only
M1   diagnostic/research only
quote current executable Bid/Ask/spread/drift/health only
```

This is a genuine scalp-horizon change from the Swing hierarchy.

## 7. Strategy floor

Retained reference families:

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

Correlation/event-lineage control prevents one market episode being counted repeatedly as independent confirmation.

## 8. Scalp geometry / freshness changes

GoldScalpTrader explicitly strengthens:

- event/trigger age;
- late-entry/chase distance;
- stale-for-entry classification;
- Approved Entry Reference versus fresh executable quote;
- gross structural room plus cost-adjusted room;
- spread/slippage/drift/latency observability;
- short-horizon time efficiency.

Swing's 1.20R Primary floor is not automatically imposed as the hard scalp floor. Exact scalp gross/net/cost thresholds remain calibration evidence questions.

## 9. Preserved Risk architecture

Automatic reference profiles remain active:

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

The current 0.50% Python scaffold is not canonical policy.

### 9.1 Aggressive small-account option

Preserved operator-requested feature:

```text
disabled by default
eligibility baseline: positive DayStartEquity < $1,000
8%  = maximum monetary SL-risk ceiling per trade, NOT target
16% = maximum aggregate open risk
16% = daily loss ceiling
```

All structural/session/news/execution safeguards remain. It never auto-enables merely from equity.

Manual daily-loss reset capability is preserved but disabled by default.

Reference cooldown/re-entry baseline is preserved: one genuinely fresh same-episode re-entry; three consecutive closed bot losses trigger at least 30 minutes global cooldown plus freshness/health release conditions.

## 10. Session / News

Scalp-specific new-entry semantics:

```text
OPEN + accepted News CLEAR    → may proceed to remaining authorities
OPEN + accepted News BLACKOUT → BLOCK
OPEN + true NEWS_SAFETY_UNKNOWN → new-entry BLOCK / LIMITED
```

Temporary provider refresh failure does not automatically create UNKNOWN:

```text
refresh fails + still-valid accepted LKG cache
→ use cached truth
→ provider may be DEGRADED
→ do not rewrite original timestamps/TTL

refresh fails + expired/invalid/no cache
→ NEWS_SAFETY_UNKNOWN
```

Preserved baseline defaults until a direct justified change/external broker fact supersedes them:

```text
Provider TTL        1800 seconds
Daily PRE_CLOSE     T-20 no entry / T-10 mandatory flatten
Weekend PRE_CLOSE   T-60 no entry / T-30 mandatory flatten
Daily reopen        1 clean completed M5
Weekend reopen      2 clean completed M5 + gap assessment
```

Current broker schedule remains external proof.

## 11. Execution capability progression

```text
READINESS / DRY_RUN
→ controlled governed DEMO writer
→ future governed REAL capability
```

REAL is **preserved as a future feature**, but disabled/unavailable until DEMO evidence, release gates and explicit operator approval satisfy its separate policy. There is no hidden REAL shortcut.

## 12. Trade management

Actions remain:

```text
HOLD
PROTECT
TRAIL
RUNNER
EXIT
```

Scalp-specific changes:

- Runner is exceptional rather than default continuation;
- time/efficiency weakness is a first-class `EXIT` reason;
- broker-valid partial management remains an optional capability where volume is divisible, but correctness at 0.01 never depends on partial close.

## 13. GitHub / backup — explicit operator changes

GitHub is source control/remote source backup only. Trading runtime has no GitHub credential and performs no Git commit/push/pull.

Development workflow:

```text
one coherent remote bulk commit
→ operator git pull --ff-only
→ local clone contains latest source + full Git history
→ optional secret-clean ZIP milestone copy
```

Runtime-state backup remains local/network-independent.

## 14. Permanent Swing → Scalp delta record

Read:

`90-governance/DOCUMENTATION_COMPARISON.md`

That file explicitly separates:

- preserved reference behaviour;
- genuine scalp-specific changes;
- explicit operator-directed changes;
- earlier unintended simplifications that have been restored.

## 15. Evidence boundary

Keep separate:

```text
FROZEN DOCUMENTED ARCHITECTURE
PRESERVED REFERENCE DEFAULT
SCALP CALIBRATION PENDING
DETERMINISTIC SOFTWARE PROOF
REPLAY / RESEARCH EVIDENCE
CONNECTED READ-ONLY PROOF
CONNECTED DEMO LIFECYCLE PROOF
FUTURE REAL RELEASE PROOF
LOCAL RECOVERY PROOF
EXTERNAL PROOF PENDING
```

No documented policy or green deterministic suite proves profitability.

## 16. Current stage

The preservation-first semantic correction is being synchronized across the affected manual. Metadata/cross-link normalization still follows before final documentation freeze.

At the **final documentation-section review**, only the remaining genuinely scalp-specific differences/thresholds will be discussed with the operator before implementation begins.