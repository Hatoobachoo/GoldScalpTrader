# GoldScalpTrader — Project Build and Recovery Guide

**Status:** DRAFT PRE-CHALLENGE AGENT OPERATING MANUAL
**Version:** 0.1-full-manual-draft
**Authority:** AI/developer build sequence, documentation-first implementation, context recovery, safe continuation and completion classification.

## 1. Mission

Work from the canonical `Documents/` manual as if the design was completed before implementation began.

Do not guess missing behaviour from nearby code, delete rationale because a new feature exists, or call a green test count project completion.

Trading behaviour remains in topic contracts. Coding quality belongs to `60-engineering/CODING_STANDARD.md`. Release proof belongs to `TESTING_AND_VERIFICATION.md` and `FINAL_RELEASE_AUDIT.md`.

## 2. Current stage rule

Before new production implementation:

```text
complete 64-file canonical manual
→ run Audit 1 fresh-zero challenge
→ resolve FIX-BEFORE-BUILD contradictions
→ synchronize affected graph
→ freeze approved architecture
→ implement in dependency order
```

The provisional code scaffold must not pull the design forward prematurely.

## 3. Agent loop

```text
ORIENT — read canonical index + authority
→ SCOPE — choose one dependency/feature
→ TRACE — owner, inputs/outputs, source/tests/docs
→ CONTRACT — states/failure/chronology/authority
→ IMPLEMENT — smallest typed change
→ VERIFY — focused + integration + quality checks
→ SYNC — full affected Documents graph
→ HANDOFF — exact evidence/limits/next step
```

Before coding answer:

- user-visible purpose;
- owning phase and contract;
- single source authority;
- input/output types, units, freshness and scope;
- independent work versus ordered authority;
- fail-closed cases;
- persistence/restart/local-backup consequences;
- operator visibility;
- research/release evidence boundary.

Never jump from feature request directly to MT5 writer code.

## 4. Source-of-truth reading order

1. `Documents/README.md`;
2. `90-governance/DOCUMENTATION_STANDARD.md`;
3. `90-governance/PRESERVATION_LEDGER.md`;
4. `00-foundation/SYSTEM_CONTRACT.md`;
5. `00-foundation/ARCHITECTURE.md`;
6. `00-foundation/BUILD_PHASES.md`;
7. relevant topic contract;
8. `DESIGN_DECISIONS.md` + `OPEN_QUESTIONS.md`;
9. `CODING_STANDARD.md`, `MODULE_STRUCTURE.md`, `FILE_AND_TEST_CATALOG.md`;
10. `CODER_GUIDE.md`;
11. current source/tests/diff/evidence.

Canonical conflict stops the affected implementation until the authority graph is repaired.

## 5. Feature packet

Every material feature/phase packet includes:

- purpose/non-goals;
- contract/authority;
- architecture and parallel/serial flow;
- implementation owner;
- stale/UNKNOWN/corrupt/ambiguous behaviour;
- persistence/restart/local-backup impact;
- positive/negative/chronology/idempotency tests;
- operator display;
- replay/learning/promotion impact;
- deterministic versus calibration/external evidence;
- affected documentation destinations.

## 6. Preservation-first protocol

For a changed rule trace:

```text
requirement
→ authoritative topic
→ decision/open question
→ architecture/state/sequence
→ source/test ownership
→ phase/coder/catalog
→ setup/user/dashboard
→ recovery/local backup
→ testing/release
→ coverage/audit/preservation
```

Do not create competing copies of policy. Supporting guides summarize; topic contract owns meaning.

## 7. Context loss / new session

Use repository truth:

```text
inspect current main HEAD
→ read canonical index/governance
→ read System Contract + Architecture
→ read affected topic/decisions/open questions
→ inspect Module Structure/File-Test Catalog
→ inspect current source/tests/diff
→ identify latest verified local checkpoint/evidence
→ continue first incomplete dependency
```

Do not restart from Phase 1 because chat context was compacted.

## 8. Interrupted implementation

1. classify deliverables DONE/PARTIAL/MISSING/BROKEN;
2. preserve and inspect current diff;
3. finish the smallest missing dependency first;
4. run focused proof before broad proof;
5. synchronize affected docs;
6. record calibration/external gaps;
7. never mark phase complete from test count alone.

## 9. Docs/code/test disagreement

| Situation | Action |
|---|---|
| frozen contract correct, code wrong | fix code + regression |
| accepted code newer, docs stale | update authority + affected graph |
| source/test map stale | correct catalog/guide/topic links |
| true design conflict | stop and classify in Decisions/Open Questions |
| historical reference differs | preserve rationale; scalp Documents remain current |
| safer code exposes stale docs | update docs; do not regress safety to prose |
| docs require missing behaviour | implement/test or explicitly classify gap |

Do not hide contradiction in UI wording, test fake, environment switch or comment.

## 10. Test failure loop

```text
reproduce
→ identify violated invariant
→ locate single owner
→ root-cause fix
→ regression
→ focused suite
→ module/integration suite
→ full local verification
→ affected graph sync
```

Never weaken safety or substitute a happy default for UNKNOWN merely to get green output.

## 11. Crash during broker write

When broker-write phase exists, if Intent is `SUBMITTING` or acknowledgement is ambiguous:

```text
DO NOT RESEND
→ restore Intent/idempotency identity
→ query broker positions/orders/deals
→ reconcile exact ticket/symbol/direction/volume/lifecycle
→ classify verified/failed/reconciling
→ create another governed Intent only after prior truth resolved
```

Broker truth outranks guessed local state.

## 12. Known ManagedTrade disappears

```text
unresolved SUBMITTING/ACCEPTED_UNKNOWN Intent?
→ reconcile first
else query exact broker exit history
→ require exact known ticket + official exit role + full original exit volume
→ incomplete/ambiguous → retain ManagedTrade + RECONCILING
→ exact close → queue + closure receipt + crash-safe clear
→ downstream exactly-once learning
```

Unknown external positions are never adopted.

## 13. Corrupt/missing runtime state

```text
block affected writes
→ preserve corrupt artifact/diagnostics
→ restore last verified full local checkpoint into NEW DB
→ connect intended MT5 account/symbol
→ reconcile positions/deals/Intents/ManagedTrade/risk/learning
→ rebuild only what evidence proves
→ remain RECONCILING/BLOCKED while critical truth unresolved
```

Never delete `.state` or invent empty exposure/zero risk as recovery.

## 14. Local full backup and new-machine recovery

Primary recovery authority is a verified **local full checkpoint/recovery package**, not GitHub.

Conceptual flow:

```text
OLD PRIMARY
→ governed safe shutdown
→ controller/MT5 write authority released
→ create + verify final local checkpoint
→ optional portable recovery package
→ transfer deliberately to NEW machine
→ restore into NEW runtime DB/path
→ configure credentials separately
→ connect same intended account/symbol
→ fresh broker positions/deals/quote/identity
→ reconcile durable lifecycle + broker truth
→ acquire local PRIMARY only after safe startup
```

A focused learning export alone is not full recovery authority.

## 15. Backup layers

```text
local working clone + .git
rolling runtime checkpoints
final graceful-shutdown checkpoint
portable recovery package
optional deliberate local Git bundle at source milestone
optional second physical drive copy
```

Automatic backup root lives outside repo. Secrets are excluded. Consistent SQLite backup is required.

## 16. No runtime Git publication

GoldScalpTrader deliberately differs from GoldSwingTraderAI:

```text
NO shutdown git add
NO shutdown git commit
NO shutdown git push
NO runtime GitHub credential requirement
```

Source control changes are deliberate development actions only.

A failed local final backup is reported explicitly after broker/controller authority is safely released. Last good durable state is preserved.

## 17. Multi-laptop rule

Per account/symbol scope:

```text
Laptop A → Account A → PRIMARY   allowed
Laptop B → Account B → PRIMARY   allowed
```

Unsupported V1:

```text
Laptop A → Account A → PRIMARY
Laptop B → same Account A → second active writer
```

Same-account movement is sequential handoff only.

Git, Drive, Dropbox or folder sync is not transactional controller fencing.

## 18. Read-only learning evidence

After a future controlled DEMO close, a reporting utility may inspect StateStore read-only and produce an evidence report for:

- DB integrity;
- closure receipt;
- matching actual DEMO observation;
- pending queue state;
- one-way scope fingerprint.

It does not initialize MT5 or write broker state.

## 19. Final audits

### Audit 1 — fresh design review

For every meaningful component classify KEEP AS-IS / SMALL IMPROVEMENT / SHOULD CHANGE / MAJOR CHANGE / REMOVE-SIMPLIFY / ADD / CALIBRATE / EXTERNAL PROOF.

### Audit 2 — Documents → Code → Tests/Evidence

For the same inventory verify canonical requirement, implementation, focused proof, failures/restart, operator meaning and external/calibration boundary.

Later corrective Audits 3–7 are evidence-triggered, not pre-filled PASS records.

## 20. Completion/handoff

A phase is complete only when:

```text
implementation exists
+ focused/full proof actually passes
+ failure/restart/learning paths explicit
+ coding standard review passes
+ source/test/catalog current
+ affected Documents synchronized
+ secret/manual gates pass
+ evidence classes remain separate
+ no critical contradiction
```

Handoff states exact revision, evidence already collected, what remains CALIBRATION/EXTERNAL and the next safe dependency.