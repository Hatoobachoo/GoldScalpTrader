# GoldScalpTrader — Canonical Documentation Manual

**Status:** DRAFT PRE-CHALLENGE MANUAL — 64-FILE INVENTORY TARGET
**Version:** 0.2-full-manual-draft
**Authority:** Entry point, reading order, document ownership and design-before-code boundary.

## 1. What this manual is

`Documents/` is the only current design, implementation and verification authority for GoldScalpTrader.

GoldScalpTrader is the scalping-specialized sibling of GoldSwingTraderAI. The reference project's engineering system, authority separation, documentation discipline, recovery philosophy, learning boundaries, audit model and parallel/serial architecture are preserved where they still make sense. Trading personality, time horizons, cost sensitivity and calibration are adapted for scalping.

No implementation convenience, chat memory, dashboard label, test fixture or reference-project threshold may silently redefine a current scalp contract.

## 2. Mandatory project method

```text
complete canonical draft manual
→ challenge it from zero
→ resolve contradictions / classify calibration and external proof
→ synchronize affected graph
→ freeze approved contracts
→ implement from contracts
→ verify Documents → Code → Tests/Evidence
→ connected DEMO/recovery proof
→ keep Documents synchronized with every material change
```

Code must not outrun the canonical manual.

## 3. Canonical reading order

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
13. all `90-governance/` decisions/open questions/preservation/documentation-control files;
14. `CODER_GUIDE.md`;
15. `PROJECT_BUILD_AND_RECOVERY_GUIDE.md`;
16. `SETUP_AND_RUN_GUIDE.md`;
17. `USER_MANUAL.md`;
18. `FINAL_BUILD_PROMPT.md`.

## 4. Canonical inventory

Expected reference-equivalent inventory:

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

The full inventory must be verified before Audit 1 is changed from `NOT RUN` to an active/completed fresh-zero review.

## 5. Architectural spine

```text
one MT5 read boundary
→ immutable MarketSnapshot
→ staged bounded-parallel market intelligence
→ independent scalp strategy-family hypotheses
→ independent BUY / SELL fusion + Red Team
→ persistent Opportunity
→ scalp Entry Timing + event freshness
→ family-aware structural TradePlan
→ independent monetary Risk
→ hard session/news/system/account/controller authorities
→ central ExecutionPermissionGate
→ durable one-shot ExecutionIntent
→ sole MT5Writer broker request
→ reconciliation against broker truth
→ ManagedTrade / Trade Manager
→ verified close
→ durable learning/research evidence
→ local backup/recovery
```

Analysis may be parallel where dependencies allow. Money, broker authority, durable intent, writer calls and reconciliation remain ordered/serial.

## 6. Scalping adaptation rule

GoldSwingTraderAI is a structural/preservation reference, not a source of blindly copied calibration.

Preserve by default:

- one normalized broker-read boundary;
- typed facts and explicit UNKNOWN states;
- causal/no-lookahead evidence;
- bounded analytical parallelism;
- independent family hypotheses and BUY/SELL debate;
- structural TradePlan before monetary Risk;
- one central execution authority;
- persist-before-send one-shot Intent;
- sole raw writer + reconciliation;
- crash-safe persistence/recovery;
- downstream learning with no direct broker authority;
- read-only operator dashboards;
- document → code → test → audit traceability.

Re-design/challenge for scalping:

- H4/H1/M15/M5/M1 roles;
- opportunity/trigger freshness;
- spread/slippage/drift/latency sensitivity;
- family decomposition/thresholds;
- entry timing and chase protection;
- structural R / target room after costs;
- risk bands for small account/minimum lot;
- hold-time/time-exit logic;
- session/news specialization;
- cost-aware replay and performance metrics.

## 7. Current major open decisions

Before implementation freeze, Audit 1 must explicitly decide at minimum:

- final timeframe/M1 authority;
- whether all six starting families remain independent;
- final `Market OPEN + News UNKNOWN` new-entry policy;
- structural R / cost-room policy;
- monetary risk profile shape and whether any aggressive mode should exist;
- exact broker-write V1 scope after DRY_RUN.

Many numerical values may remain `CALIBRATION PENDING` even after architecture freezes.

## 8. GitHub / zero-cost boundary

GitHub is deliberate source control/remote source backup only.

The architecture does not require:

- GitHub Actions;
- Codespaces;
- Git LFS;
- paid Marketplace services;
- paid cloud compute;
- paid external APIs.

The trading runtime has no GitHub credential or automatic publication authority.

## 9. Local backup boundary

GoldScalpTrader is designed to remain recoverable without GitHub availability.

```text
local working clone + .git
→ rolling runtime checkpoints
→ graceful-shutdown final verified local checkpoint
→ portable local recovery package
→ optional deliberate local Git bundle at source milestone
→ optional second physical drive copy
```

Automatic backup paths live outside the working repository.

`.env`, passwords, tokens, MT5 credentials, GitHub PATs/private keys and credential-bearing URLs are excluded from automatic recovery artifacts.

Graceful shutdown may create local state backup. It must not perform Git commit/push.

## 10. Evidence boundary

Keep separate:

```text
DRAFT / FROZEN DOCUMENTED DESIGN
DETERMINISTIC SOFTWARE PROOF
REPLAY / RESEARCH EVIDENCE
CONNECTED READ-ONLY PROOF
CONNECTED DEMO LIFECYCLE PROOF
LOCAL RECOVERY PROOF
CALIBRATION PENDING
EXTERNAL PROOF PENDING
```

A green deterministic suite does not prove current broker connectivity, realistic execution, future edge or profitability.

## 11. Current status and next phase

The canonical tree is being finalized as a complete **DRAFT PRE-CHALLENGE** manual.

Once exact 64/64 inventory and cross-links are verified, the next phase is **`60-engineering/AUDIT_1_FRESH_DESIGN_REVIEW.md`**:

> If GoldScalpTrader were designed today from zero, what would we keep, improve, change, remove or add?

Only after that review and affected-graph synchronization do accepted contracts become frozen for implementation.