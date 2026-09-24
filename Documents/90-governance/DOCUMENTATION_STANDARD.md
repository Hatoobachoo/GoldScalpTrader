# GoldScalpTrader — Documentation Standard

**Status:** DRAFT PRE-CHALLENGE DOCUMENTATION GOVERNANCE
**Version:** 0.1-canonical-method
**Authority:** Documentation ownership, synchronization, quality, affected-graph control and durable project truth.

## 1. Purpose

GoldScalpTrader is documentation-first. The repository is implemented from contracts, not undocumented assumptions.

Before changing code, a developer or AI must be able to answer:

- Why does this subsystem exist?
- What inputs does it accept?
- What output/state does it produce?
- Which work may happen independently or in parallel?
- Which authority must happen in strict order?
- What happens on stale, missing, corrupt or UNKNOWN truth?
- What survives restart/restore/machine migration?
- What does the operator see?
- Which source files and tests implement/prove it?
- Which research, backup and release documents are affected?

## 2. Canonical folder rule

`Documents/` is the only active documentation authority.

Do not create a second lowercase `docs/` manual or another parallel source of current product truth.

Historical/superseded reasoning belongs in governance records and Git history, not in a competing active contract tree.

## 3. One behavioural owner

Every material rule has one authoritative topic contract.

Other documents may summarize, link or explain it but must not silently redefine it.

Examples:
- project purpose → `00-foundation/PROJECT_VISION.md`;
- top-level invariants → `00-foundation/SYSTEM_CONTRACT.md`;
- topology/concurrency → `00-foundation/ARCHITECTURE.md`;
- strategy-family ownership → `20-trading-decisions/STRATEGY_FLOOR.md`;
- structural entry/stop/targets → `20-trading-decisions/TRADE_PLAN.md`;
- monetary risk → `30-risk-execution/RISK_CONTRACT.md`;
- restart/recovery → `30-risk-execution/PERSISTENCE_RESTART_AND_RECOVERY.md`;
- local backup/machine portability → `40-research-learning/LEARNING_BACKUP_AND_MULTI_MACHINE.md` plus recovery contract for runtime state;
- code placement → `60-engineering/MODULE_STRUCTURE.md`;
- documentation method → this file.

## 4. Document contract shape

Where applicable, a topic document should state:

1. Status/version/authority.
2. Purpose and boundary.
3. Inputs.
4. Outputs/state.
5. Invariants.
6. Dependency/flow diagram or ordered text path.
7. Allowed influence.
8. Forbidden authority.
9. Failure/UNKNOWN behaviour.
10. Persistence/restart consequence.
11. Parallel/serial semantics.
12. Operator/dashboard consequence.
13. Research/replay consequence.
14. Implementation owner(s).
15. Test/evidence owner(s).
16. Calibration/external-proof items.
17. Links to affected contracts.

Not every file needs identical headings, but no critical semantic area should be implicit.

## 5. Preserve rationale, not obsolete ambiguity

When behaviour changes:

- current topic contract becomes unambiguous;
- old rationale remains visible through `DESIGN_DECISIONS.md`, audit records or Git history;
- superseded behaviour must not remain written as if active;
- summaries/manuals must be synchronized.

## 6. Full affected-graph update rule

A material change is not documented when only the nearest file is updated.

The author must inspect the full affected graph:

```text
Code or contract change
        |
        v
Authoritative topic owner
        |
        +--> Design Decision / Open Question
        +--> System/Runtime Architecture
        +--> Trading Floor / lifecycle documents
        +--> Module Structure / File-Test Catalog
        +--> Coder / Build / Setup guides
        +--> Persistence / Backup / Recovery
        +--> Dashboard / Diagnostics
        +--> Research / Learning
        +--> Release Checklist / Audits
        +--> Glossary / README when navigation or terminology changes
```

Only actually affected documents need text changes, but all relevant surfaces must be consciously checked.

## 7. Before implementation

For a coherent feature/change packet:

1. identify the behavioural owner;
2. classify it as existing decision, new decision or open question;
3. resolve any FIX-BEFORE-BUILD ambiguity;
4. define typed inputs/outputs/state;
5. define failure and UNKNOWN semantics;
6. define parallel versus ordered work;
7. define persistence/restart impact;
8. define operator/research impact;
9. define source/test ownership;
10. identify affected documentation graph.

## 8. During implementation

1. implement only documented behaviour;
2. keep hard-authority boundaries intact;
3. update source/entry-point/test ownership if the actual design changes;
4. synchronize persistence/dashboard/research/release consequences;
5. preserve superseded rationale through governance records;
6. run focused verification;
7. run broader structural verification when the change crosses module boundaries.

If implementation reveals a wrong assumption, update the contract/decision before accepting the changed code as canonical.

## 9. Before handoff/completion claim

1. read affected documents end-to-end;
2. check source/test inventory and links;
3. verify terminology against Glossary;
4. verify no parallel authority was accidentally introduced;
5. distinguish deterministic proof from connected/calibration proof;
6. perform reconstructability review: could another capable developer continue without chat history?
7. record open items accurately;
8. synchronize the final affected graph.

## 10. Documentation change packet

Each material packet should be traceable through:

| Field | Required meaning |
|---|---|
| Behaviour owner | authoritative topic file |
| Preserved meaning | rationale/invariants intentionally retained |
| New truth | decision/state/evidence change |
| Affected graph | documents inspected/updated |
| Source map | files/classes/entry points once implemented |
| Tests/evidence | deterministic versus external/calibration |
| Diagram impact | updated or explicitly unchanged |
| Reconstructability | continuation possible without chat history |
| Open items | exact remaining work |

## 11. AI/ChatGPT working rule

Before implementing a material feature, the AI/developer must:

1. read `Documents/README.md` and the relevant authority contracts;
2. read `CODER_GUIDE.md`, `60-engineering/MODULE_STRUCTURE.md` and `60-engineering/CODING_STANDARD.md` once those files exist;
3. inspect current source/tests and latest repository state;
4. identify the affected graph;
5. implement one coherent packet;
6. run focused/full verification as appropriate;
7. synchronize Documents before claiming completion;
8. keep durable project truth in repository documents, not chat memory.

If code, tests and Documents disagree, classify and repair the contradiction rather than guessing which one “probably” wins.

## 12. Scalping-specific documentation rule

Scalp contracts must be explicit where a short horizon changes semantics, especially:

- timeframe authority;
- completed versus forming/tick evidence;
- event/trigger freshness;
- Bid/Ask/executable geometry;
- spread/slippage/cost assumptions;
- opportunity expiry and re-arm;
- time-based exits;
- high-frequency risk-day interactions;
- backtest transaction-cost assumptions;
- latency/freshness diagnostics.

Do not hide these differences behind generic “same as Swing” wording.

## 13. Local backup documentation rule

Backup is a cross-cutting recovery surface.

Any change to durable state, schema, learning artifacts, source packaging or restore order must check:

- `PERSISTENCE_RESTART_AND_RECOVERY.md`;
- `LEARNING_BACKUP_AND_MULTI_MACHINE.md`;
- module/file catalogs;
- setup/build/recovery guides;
- release checklist/audit;
- security/secret-exclusion rules.

No shutdown-GitHub-push behaviour is part of the target project.

## 14. Quality gates

Documentation fails review if it:

- relies on chat history for a rule missing from `Documents/`;
- uses vague words such as “safe”, “fresh”, “low spread” or “good setup” without naming the owning contract;
- duplicates authority in two topic files;
- hides UNKNOWN/error behaviour;
- confuses analytics with broker permission;
- confuses backtest success with live readiness/profitability;
- moves a rule without updating links/ownership;
- updates only one file when the affected graph is larger;
- lets a dashboard/prompt/checklist override a topic contract;
- introduces implementation details that contradict the source/test map;
- silently copies Swing calibration into the scalp project without challenge.

## 15. Freeze rule

This documentation method will itself be challenged before final freeze. Once frozen, changing it requires a governance decision and preservation review.
