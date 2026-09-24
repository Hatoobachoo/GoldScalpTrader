# GoldScalpTrader — Canonical Documentation Manual

**Status:** DRAFT PRE-CHALLENGE MANUAL
**Version:** 0.1-foundation
**Authority:** Entry point, reading order, document ownership and design-before-code boundary.

## 1. What this manual is

`Documents/` is the only current design and implementation authority for GoldScalpTrader.

GoldScalpTrader is intentionally being designed as the scalping-specialized sibling of GoldSwingTraderAI. The engineering system, authority separation, documentation discipline, recovery philosophy, learning boundaries, audits and parallel/serial runtime model are preserved unless a scalp-specific challenge proves a change is necessary.

No implementation convenience may silently redefine a documented rule. Chat history is not durable project authority.

## 2. Project method

The mandatory project sequence is:

1. decide architecture and product behaviour;
2. write the complete interconnected canonical manual;
3. challenge the manual from zero and against Gold scalping realities;
4. resolve contradictions and open questions;
5. freeze approved contracts;
6. implement from those contracts;
7. verify code against documents and tests;
8. keep the affected document graph synchronized with every material change.

Code must not outrun the canonical manual.

## 3. Canonical reading order

1. `README.md` and `GLOSSARY.md`;
2. `00-foundation/PROJECT_VISION.md`;
3. `00-foundation/SYSTEM_CONTRACT.md`;
4. `00-foundation/ARCHITECTURE.md`;
5. `00-foundation/TRADING_FLOOR_ARCHITECTURE.md`;
6. `00-foundation/BUILD_PHASES.md`;
7. `10-market-intelligence/` contracts;
8. `20-trading-decisions/` contracts;
9. `30-risk-execution/` contracts;
10. `40-research-learning/` contracts;
11. `50-operator/` contracts;
12. `60-engineering/` standards, catalogs, tests and audits;
13. `90-governance/` decisions, open questions, preservation and documentation control;
14. top-level setup, coder, recovery, user and final-build guides.

## 4. Architectural spine

The intended governed production path is:

```text
one MT5 read boundary
→ immutable MarketSnapshot
→ staged bounded-parallel market intelligence
→ independent scalp strategy-family hypotheses
→ independent BUY / SELL fusion
→ persistent Opportunity
→ scalp Entry Timing
→ family-aware structural Trade Plan
→ independent monetary Risk
→ hard session/news/system/account/controller authorities
→ central Execution Permission Gate
→ durable one-shot ExecutionIntent
→ sole MT5Writer broker request
→ reconciliation against broker truth
→ post-entry Trade Manager
→ verified close accounting
→ durable learning/research evidence
```

Analysis may be parallel where dependencies permit. Money, broker authority, durable intent, writes and reconciliation remain ordered and serial.

## 5. Scalping adaptation rule

GoldSwingTraderAI is the structural reference, not a source of blindly copied trading calibration.

Preserve by default:
- one normalized broker-read boundary;
- typed facts and explicit UNKNOWN states;
- causal/no-lookahead evidence;
- bounded analytical parallelism;
- independent strategy families and BUY/SELL debate;
- structural Trade Plan before monetary Risk;
- one central execution permission authority;
- persist-before-send one-shot Intent;
- sole raw broker writer and reconciliation;
- crash-safe persistence/recovery;
- downstream learning with no direct broker authority;
- read-only operator dashboards;
- document → code → test → audit traceability.

Re-design for scalping where evidence requires:
- timeframe roles;
- opportunity and trigger freshness;
- spread/slippage/executable-price geometry;
- strategy-family hypotheses;
- entry timing and late-entry protection;
- target/stop/holding-time logic;
- re-arm/cooldown behaviour;
- session specialization;
- cost-aware research and performance metrics.

## 6. GitHub and billing boundary

GitHub is source control and remote project backup only.

The architecture does not require:
- GitHub Actions;
- Codespaces;
- Git LFS;
- paid Marketplace apps;
- paid cloud compute;
- paid external APIs.

The bot runtime must not automatically push to GitHub on graceful shutdown.

No runtime GitHub token, repository credential or autonomous publication authority is required for trading.

## 7. Local backup boundary

GoldScalpTrader also maintains a GitHub-independent local recovery design.

Three distinct layers are planned:

1. **Local working clone** — source + normal local Git history.
2. **Rolling runtime backup** — durable trading/runtime/research state snapshots stored outside the repository working tree.
3. **Portable recovery package** — controlled local package capable of reconstructing source/history plus verified runtime state without requiring GitHub access.

Default local backup paths must live outside the repository to avoid recursive archives and accidental commits.

`.env`, passwords, tokens, MT5 credentials and other secrets are never automatically included in source/recovery archives.

Graceful shutdown may create a local state backup. It must not perform a GitHub push.

## 8. Evidence boundary

A passing deterministic test proves only the exercised software contract. It does not prove current broker connectivity, execution quality, future edge or profitability.

Claims must remain classified as deterministic proof, replay/research evidence, connected broker proof, calibration pending or external proof pending.

## 9. Current status

This manual is intentionally `DRAFT PRE-CHALLENGE`.

Foundation and governance contracts are being written first. Trading calibration is not frozen yet. The later fresh-from-zero challenge may KEEP, MODIFY, REMOVE, ADD or defer individual design choices before implementation begins.
