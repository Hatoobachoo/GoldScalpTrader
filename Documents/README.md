# GoldScalpTrader — Canonical Documentation Manual

**Status:** AUDIT 1 COMPLETE — POST-CHALLENGE AFFECTED-GRAPH SYNCHRONIZATION
**Version:** 1.0-fresh-zero-architecture
**Authority:** Entry point, reading order, document ownership and design-before-code boundary.

## 1. What this manual is

`Documents/` is the only current design, implementation and verification authority for GoldScalpTrader.

GoldScalpTrader is the scalping-specialized sibling of GoldSwingTraderAI. The reference project's engineering system, authority separation, documentation discipline, recovery philosophy, learning boundaries, audit model and parallel/serial architecture are preserved where the fresh-zero review found them sound. Trading personality, time horizons, cost sensitivity and calibration are scalp-specific.

No implementation convenience, chat memory, dashboard label, test fixture or reference threshold may silently redefine a current contract.

## 2. Project method

```text
complete canonical draft manual
→ Audit 1 fresh-zero challenge            COMPLETE
→ synchronize affected graph              CURRENT PACKET
→ freeze accepted architecture contracts
→ implement from contracts
→ verify Documents → Code → Tests/Evidence
→ connected DEMO/recovery proof
→ keep Documents synchronized with every material change
```

Code must not outrun the canonical manual.

## 3. Canonical inventory

Reference-equivalent inventory is preserved:

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

Audit 1 was run only after this inventory was present.

## 4. Canonical reading order

1. `README.md` and `GLOSSARY.md`;
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
12. `60-engineering/CODING_STANDARD.md`, `MODULE_STRUCTURE.md`, `FILE_AND_TEST_CATALOG.md`, testing/health/release/audits;
13. all `90-governance/` files;
14. `CODER_GUIDE.md`;
15. `PROJECT_BUILD_AND_RECOVERY_GUIDE.md`;
16. `SETUP_AND_RUN_GUIDE.md`;
17. `USER_MANUAL.md`;
18. `FINAL_BUILD_PROMPT.md`.

When documents conflict, system-wide invariant → topic owner → active Design Decision → Open Question classification → Architecture → engineering/documentation guides.

## 5. Fresh-zero architecture verdict

The core remains:

```text
one MT5 read boundary
→ immutable MarketSnapshot
→ staged independent market intelligence
→ six independent scalp strategy-family hypotheses
→ independent BUY / SELL fusion + Red Team
→ persistent Opportunity
→ completed-M5 Entry Timing + event freshness
→ family-aware structural TradePlan
→ gross + cost-adjusted room truth
→ independent monetary Risk
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

Analysis is logically parallel where dependencies allow. Actual concurrent workers are optional/profiling-driven. Money, broker authority, durable Intent, writer calls and reconciliation remain serial.

## 6. Frozen V1 timeframe roles

```text
H1   broad soft regime / major directional-volatility context
M15  opportunity location, path, liquidity/session context
M5   primary completed-bar setup, entry timing and normal management
H4   optional major context only
M1   diagnostic/research only
quote current executable Bid/Ask/spread/drift/health only
```

M1 is not a hidden production trigger timeframe in V1.

## 7. Six-family floor

Retained after fresh-zero review:

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

Family overlap is handled with correlation/event-lineage bounding, not by requiring unanimity or counting correlated labels as independent certainty.

## 8. Cost-aware scalp geometry

A structurally attractive chart is not enough. TradePlan must preserve:

```text
gross structural geometry
+ current known transaction-cost context
+ cost-adjusted remaining room
```

Execution separately rechecks the fresh executable quote/spread/drift immediately before send. Costs are never double counted and stop/target are never moved to manufacture acceptable R.

The old Swing 1.20R floor is not active scalp policy. Exact gross/net thresholds remain calibration pending.

## 9. Risk architecture

V1 uses one explicit `STANDARD` production risk policy rather than automatic SMALL/MEDIUM/NORMAL equity tiers.

Actual account size still matters through verified equity, structural stop, tick value and broker minimum/step volume.

The STANDARD policy owns preferred per-trade risk target, hard ceiling, daily loss limit, one-position capacity and durable loss/cooldown/re-entry state. Numerical values remain calibration pending.

Historical aggressive 8%/16% small-account values are not active V1 policy. Any future aggressive experiment is explicit, research-governed and disabled by default.

## 10. Session / News V1 rule

```text
Session OPEN + News CLEAR    → may proceed to other authorities
Session OPEN + News BLACKOUT → hard new-entry BLOCK
Session OPEN + News UNKNOWN  → new-entry BLOCK / visibly limited
```

News UNKNOWN never becomes CLEAR. Existing-position management/protection/mandatory CLOSE remains action-sensitive.

## 11. Execution scope

```text
READINESS / DRY_RUN
→ controlled governed DEMO writer after implementation + deterministic proof
REAL → outside V1; separate future governance decision
```

One-shot Intent, sole writer and reconciliation remain non-negotiable.

## 12. Management scope

V1 action vocabulary remains:

```text
HOLD
PROTECT
TRAIL
RUNNER
EXIT
```

Time/efficiency is a first-class `EXIT` reason, not a separate TIME_EXIT action. Runner is exceptional rather than the default scalp objective.

## 13. GitHub / zero-cost boundary

GitHub is deliberate source control/remote source backup only.

The architecture does not require GitHub Actions, Codespaces, LFS, paid Marketplace services, paid cloud compute or paid external APIs.

The trading runtime has no GitHub credential or automatic publication authority.

## 14. Local development backup

Normal low-GitHub-use workflow after a major bulk:

```text
one coherent remote commit
→ operator runs git pull --ff-only
→ local clone now has complete source + Git history
→ optional secret-clean local ZIP snapshot for extra offline copy
```

A Git bundle is optional advanced/manual tooling, not the default path.

Runtime state backup is separate from source backup and remains local/network-independent.

## 15. Evidence boundary

Keep separate:

```text
FROZEN DOCUMENTED ARCHITECTURE
CALIBRATION PENDING NUMBERS
DETERMINISTIC SOFTWARE PROOF
REPLAY / RESEARCH EVIDENCE
CONNECTED READ-ONLY PROOF
CONNECTED DEMO LIFECYCLE PROOF
LOCAL RECOVERY PROOF
EXTERNAL PROOF PENDING
```

A green deterministic suite does not prove current broker connectivity, execution quality, future edge or profitability.

## 16. Current status / next dependency

`AUDIT_1_FRESH_DESIGN_REVIEW.md` is complete. Core affected contracts are being synchronized to its decisions.

Implementation must not start until this synchronization packet is complete and no canonical contradiction remains.

After that, the first implementation dependency is foundation/package/read-truth work, not broker order execution.