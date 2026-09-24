# GoldScalpTrader — Documentation Standard

**Status:** ACTIVE DOCUMENTATION GOVERNANCE — PRESERVATION-FIRST / PRE-IMPLEMENTATION FREEZE PREPARATION
**Version:** 1.0-preservation-first-governance
**Authority:** Documentation ownership, reference preservation, synchronization, quality, change control and reconstructability.

## 1. Canonical authority

`Documents/` is the sole current documentation authority for GoldScalpTrader.

Chat memory, provisional source, dashboard wording, test fixtures and GoldSwingTraderAI reference files cannot silently override current Scalp contracts.

GoldSwingTraderAI nevertheless remains the **default feature/default preservation baseline**.

## 2. Preservation-first rule

An inherited reference feature/default may differ in GoldScalpTrader only when at least one is true:

1. a direct scalping requirement justifies it;
2. the operator explicitly instructs the difference;
3. a separately proven reference defect requires correction.

A simpler design, smaller implementation or personal design preference is not enough.

If classification is uncertain:

```text
preserve reference behaviour now
→ record proposed difference/question
→ discuss during final documentation review
→ change only through governed affected-graph packet
```

## 3. Delta classification

Every material reference difference is classified as one of:

```text
PRESERVED REFERENCE DEFAULT
SCALP-SPECIFIC CHANGE
OPERATOR-DIRECTED CHANGE
REFERENCE DEFECT CORRECTION
EXTERNAL FACT UPDATE
```

`DOCUMENTATION_COMPARISON.md` is the durable explicit delta ledger. `PRESERVATION_LEDGER.md` records preservation status.

An `EXTERNAL FACT UPDATE` such as a broker schedule/spec change is not automatically a strategy/policy redesign.

## 4. One behavioural rule = one owner

Examples:

- timeframe authority → Architecture / Market/Decision contracts;
- monetary profile bands/aggressive mode → `RISK_CONTRACT.md`;
- News cache/provider acquisition → `SESSION_NEWS_PROVIDER_CONTRACT.md`;
- permission composition → `SESSION_AND_RISK_STATE_MACHINE.md` / Risk permissions;
- execution one-shot rules → execution contract;
- Trade Manager actions → `TRADE_MANAGER_AND_EXIT.md`;
- source ownership → Module Structure/File-Test Catalog.

Summary/manual files must reflect, not redefine, topic owners.

## 5. Material change affected graph

For a material change inspect/update as applicable:

```text
topic owner
→ DESIGN_DECISIONS / OPEN_QUESTIONS
→ DOCUMENTATION_COMPARISON / PRESERVATION_LEDGER if inherited behaviour changes
→ SYSTEM_CONTRACT / Architecture / lifecycle
→ Module Structure / File-Test Catalog
→ Coder / Build / Setup / User / Final Build manuals
→ operator/research/recovery consequences
→ Testing / Release / Audit surfaces
→ Content Coverage / Documentation Audit
```

A material change is incomplete while any affected canonical surface states old behavior.

## 6. Reference-delta change packet

A proposed inherited-behaviour change must state:

```text
reference behaviour/default
current Scalp behaviour
classification (scalp/operator/defect/external fact)
reason/evidence
authority owner
risk/execution consequence
persistence/restart consequence
operator consequence
research consequence
test/evidence route
rollback/supersession impact
```

Without this classification, preserve the reference behavior.

## 7. Scalp-specific calibration discipline

Only genuinely scalp-sensitive values should be automatically treated as scalp calibration questions, for example:

- event/trigger age and chase distance;
- gross vs cost-adjusted target quality;
- spread/slippage/drift thresholds;
- latency thresholds;
- time-efficiency EXIT rules;
- Runner/Expansion scalp policy;
- session conditioning of scalp expectancy;
- event blackout/post-news stabilization where scalp evidence specifically justifies a change.

Non-scalp reference defaults are not reopened just because the product is a scalper.

## 8. Evidence/status discipline

Use truthful states such as:

```text
DRAFT
FROZEN
PRESERVED REFERENCE DEFAULT
SCALP CALIBRATION PENDING
IMPLEMENTATION PENDING
IMPLEMENTED
DETERMINISTIC PROOF PENDING/PASS
EXTERNAL PROOF PENDING
NOT RUN
```

Do not mark implementation/test/DEMO evidence complete merely because architecture is frozen.

## 9. Metadata requirements

Every substantive document should include:

```text
Status
Version
Authority
```

Metadata must reflect the current project stage. Legacy `DRAFT PRE-CHALLENGE` headers must be normalized before documentation freeze when Audit 1 has already accepted/preserved their architecture.

## 10. Reconstructability rule

A capable new developer/AI with no chat history must be able to determine from the repository:

- project purpose/non-goals;
- preserved Swing features/defaults;
- genuine Scalp deltas;
- operator-directed differences;
- unresolved scalp calibration/external proof;
- exact authority/source/test ownership;
- runtime/source recovery process;
- current implementation/evidence state.

If chat history is needed to know a material rule, documentation is incomplete.

## 11. No code ahead of documents

```text
contract / decision
→ affected-graph sync
→ implementation
→ deterministic proof
→ connected proof where required
→ documentation/evidence update
```

Code may not become the de facto design source because a document was inconvenient.

## 12. Low-GitHub-use development workflow

Documentation/code work should be grouped into large coherent logical packets when practical:

```text
many related file changes
→ one consolidated fast-forward Git commit
→ one operator git pull --ff-only checkpoint
```

Avoid noisy microcommits/pulls merely for convenience.

Trading runtime itself performs no Git operation.

## 13. Final documentation review

Before implementation freeze:

1. full affected graph is synchronized;
2. metadata/cross-links are normalized;
3. `DOCUMENTATION_AUDIT.md` reconstructability checks are clean;
4. operator is shown the remaining **genuinely scalp-specific** changes/threshold questions;
5. non-scalp features/defaults are not reopened unless operator explicitly chooses to discuss/change them.

Only then is documentation freeze declared complete.