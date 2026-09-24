# GoldScalpTrader — Documentation Standard

**Status:** DRAFT PRE-CHALLENGE DOCUMENTATION GOVERNANCE
**Version:** 0.2-full-manual-draft
**Authority:** Documentation ownership, preservation, synchronization, quality and change control.

## 1. Purpose

GoldScalpTrader is documentation-first. The repository is implemented from contracts, not undocumented assumptions.

Before changing code a developer/AI must be able to answer:

- why the subsystem exists;
- its inputs/outputs/state;
- which work is independent/parallel;
- which authority is ordered/serial;
- stale/missing/corrupt/UNKNOWN behaviour;
- restart/restore/migration semantics;
- operator visibility;
- implementation/test ownership;
- research/backup/release consequences.

Behaviour belongs to topic contracts. This standard owns how truth is maintained.

## 2. Canonical documentation authority

```text
Documents/ = only active project manual
chat memory = convenience context, never durable authority
root README = project entry only, not competing behaviour manual
```

No parallel lowercase `docs/` authority is created.

Historical rationale remains in Git history/governance records rather than active contradictory manuals.

## 3. Required metadata

Substantive canonical files include:

```text
Status
Version
Authority
```

Status language must distinguish DRAFT, FROZEN, IMPLEMENTED, NOT RUN, CALIBRATION PENDING and EXTERNAL PROOF PENDING truthfully.

Do not mark a feature implemented because its document exists.

## 4. One behavioural owner

Every meaningful rule has one canonical owner.

Other documents summarize/link rather than silently redefine it.

Examples:

```text
completed-candle chronology → MARKET_DATA/CANDLE_STRUCTURE
family hypotheses           → STRATEGY_FLOOR
entry lifecycle             → ENTRY_TIMING
structural geometry         → TRADE_PLAN + family extensions
monetary affordability      → RISK_CONTRACT
session/news permission     → SESSION_AND_RISK_STATE_MACHINE
broker lifecycle            → EXECUTION_AND_BROKER_SAFETY
backup/recovery             → PERSISTENCE_RESTART_AND_RECOVERY
learning boundaries         → LEARNING_AND_AI_BOUNDARIES
operator meaning            → DASHBOARD_AND_UX
```

## 5. Preserve rationale without preserving obsolete truth

If a decision is superseded:

- current topic contract becomes unambiguous;
- `DESIGN_DECISIONS.md` keeps historical rationale/status;
- `OPEN_QUESTIONS.md` updates if evidence is pending;
- Git history preserves old text.

Do not leave obsolete behaviour active merely because it was historically important.

## 6. Full affected-graph rule

A material change is not documented when only the nearest file changes.

```text
change
→ authoritative topic
→ Design Decision / Open Question
→ System/Architecture/lifecycle impact
→ Module/File-Test/Coder/Build map
→ Persistence/recovery effect
→ Operator/diagnostics effect
→ Research/learning effect
→ Testing/release/audit evidence
```

Inspect all relevant nodes even when some remain unchanged; record why where useful.

## 7. Change packet

A coherent packet records:

| Field | Required content |
|---|---|
| Behaviour owner | authoritative file |
| Preserved meaning | retained rationale/invariant |
| New truth | semantic change |
| Affected graph | synchronized docs |
| Source map | planned/actual files/classes/entry points |
| Tests/evidence | deterministic vs replay vs external |
| Persistence/recovery | state/restore/backup consequence |
| Operator impact | visible meaning |
| Research impact | replay/learning/promotion consequence |
| Reconstructability | continuation without chat history |
| Open items | exact remaining work |

## 8. Documentation-first build loop

Before implementation:

1. read `Documents/README.md` and relevant topic owners;
2. read `CODER_GUIDE.md`, `MODULE_STRUCTURE.md`, `CODING_STANDARD.md`;
3. identify one coherent feature/dependency;
4. classify decisions/open questions;
5. define source/test/failure ownership;
6. identify affected-document graph;
7. ensure implementation is not starting ahead of unresolved FIX-BEFORE-BUILD questions.

During implementation:

1. implement from the authoritative contract;
2. keep deterministic/typed ownership;
3. update source/test maps;
4. update persistence/operator/research/release consequences;
5. preserve superseded rationale;
6. run focused/full verification.

Before handoff:

1. reread affected files end-to-end;
2. inspect source/test inventory/links;
3. classify evidence honestly;
4. perform reconstructability review;
5. record remaining external/calibration proof.

## 9. AI/ChatGPT working rule

For any material change:

```text
read canonical authority
→ inspect current repository/source/tests
→ state/understand affected graph
→ implement one coherent packet
→ verify
→ synchronize Documents
→ retain durable truth in repository
```

If code/tests/Documents disagree, classify and repair contradiction rather than guessing.

AI may not use chat history to override canonical current files.

## 10. Scalping-specific synchronization hotspots

The following changes are especially cross-cutting:

### Timeframe/M1 role

Touches Market Data, Candle Structure, Technical/Liquidity/Quant, Strategy Floor, Entry Timing, Architecture, Research/Replay, Dashboard, Coder/Testing.

### Risk percentages / min lot

Touches Risk, System Contract, Trade Plan boundary, dashboard, config, tests, research and release.

### News UNKNOWN policy

Touches Fundamental/News, Provider, Session/Risk state, Execution Gate, Health, dashboards, tests/replay and manuals.

### Structural R / cost threshold

Touches TradePlan, timing, strategy/fusion context, Risk boundary, audits, dashboards, replay/research and tests.

### Local backup

Touches Persistence, Learning Backup, Module Structure, Coder/Setup/Build guides, health, release/audits and scripts.

### Broker-write implementation

Touches System Contract, Execution, Risk/Session, Recovery, Controller, Management, local backup, dashboards, testing/release/user manuals.

## 11. Diagrams and terminology

Diagrams are architecture aids and must match current prose ownership.

Canonical terms are defined in `GLOSSARY.md`; topic contracts may add precision but must not silently redefine hard-authority meaning.

## 12. Cross-links and path truth

Document links/paths must point to current canonical files.

When source paths are only planned, say `planned` until implementation creates them.

Do not cite nonexistent tests as passing proof.

## 13. Evidence wording

Approved claim categories:

```text
DOCUMENTED / DRAFT
FROZEN DESIGN
IMPLEMENTED
DETERMINISTICALLY VERIFIED
REPLAY/RESEARCH EVIDENCE
CONNECTED READINESS VERIFIED
CONNECTED DEMO VERIFIED
LOCAL RECOVERY VERIFIED
CALIBRATION PENDING
EXTERNAL PROOF PENDING
```

Never convert a lower evidence rung into a higher one by wording.

## 14. Backup/publication documentation rule

GoldScalpTrader's current design is local-backup-first:

- graceful runtime shutdown may create local verified checkpoint/package;
- trading runtime does not Git commit/push;
- source Git commits happen through deliberate development workflow;
- local Git bundle is an optional deliberate source-history backup;
- backup packages exclude secrets.

Any future reversal of this boundary requires explicit governance decision and full affected-graph review.

## 15. Quality gates

Do not:

- add code with no documented behavioural owner;
- update one doc when affected graph is larger;
- let dashboard/prompt/checklist override topic contract;
- call unit tests external broker proof;
- invent missing source/test evidence;
- recreate a parallel manual;
- rely on chat memory for a rule absent from `Documents/`;
- mark audit PASS before it is run.

## 16. Freeze process

Current manual remains `DRAFT PRE-CHALLENGE` until:

1. 64-file reference-equivalent inventory is complete;
2. `AUDIT_1_FRESH_DESIGN_REVIEW.md` challenges every major component;
3. contradictions/open questions are resolved/classified;
4. affected docs are synchronized;
5. reconstructability/documentation audit passes;
6. accepted architecture is explicitly frozen for implementation.

Changing this maintenance method after freeze requires governance decision plus preservation review.
