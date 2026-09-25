# GoldScalpTrader — Legacy Docs Retirement

**Status:** FINAL GOVERNANCE RECORD — SINGLE CANONICAL DOCUMENTATION TREE
**Version:** 2.0-single-authority-final
**Authority:** Prevent parallel/conflicting manuals and define treatment of historical/reference documentation.

## 1. Canonical authority

```text
Documents/       = one current active project manual
lowercase docs/  = must not become a competing active manual
Git history      = prior revision history
GoldSwingTraderAI reference = external preservation/depth baseline, not current runtime authority
```

## 2. Current repository state

No separate historical lowercase `docs/` product manual is part of the intended architecture.

The final current numbered categories are:

```text
01-foundation
02-market-intelligence
03-trading-decisions
04-risk-execution
05-research-learning
06-operator
07-engineering
08-governance
```

Old `00/10/20/30/40/50/60/90` paths are legacy path names after the final migration and must not be recreated as a second tree.

## 3. Why this record exists

Documentation defects are dangerous when several files claim authority for the same topic.

Prohibited state:

```text
Documents/01... with rule A
+ old Documents/00... duplicate with rule B
+ lowercase docs/ with rule C
+ stale top-level prompt with rule D
```

The project must keep one active truth graph.

## 4. Historical material handling

If legacy/reference material is found later:

```text
inventory
→ compare against current canonical owner
→ preserve useful rationale/features/defaults
→ classify difference as preserved / Scalp / operator / defect / factual update
→ migrate useful content into canonical Documents
→ update Comparison / Preservation Ledger / Coverage Matrix
→ retire duplicate active authority
```

Do not delete useful historical rationale merely for tidiness; Git history may preserve superseded revisions after current truth is migrated.

## 5. GoldSwingTraderAI relationship

GoldSwingTraderAI remains a reference/preservation baseline.

It does not override a current GoldScalpTrader contract where an accepted Scalp-specific or operator-directed difference exists.

Exact relationship is owned by:

```text
08-governance/DOCUMENTATION_COMPARISON.md
08-governance/PRESERVATION_LEDGER.md
```

## 6. Top-level manuals

`README.md`, `GLOSSARY.md`, `CODER_GUIDE.md`, `PROJECT_BUILD_AND_RECOVERY_GUIDE.md`, `FINAL_BUILD_PROMPT.md`, `USER_MANUAL.md`, `SETUP_AND_RUN_GUIDE.md`, `GITHUB_STRICT_USE_POLICY.md` and `BACKUP_SYNC_AND_RECOVERY_ARCHITECTURE.md` summarize/navigate canonical topic contracts.

They may not silently override the topic owner.

## 7. Folder migration rule

After the approved `01`–`08` migration:

- old numbered paths are invalid current links;
- every relative link must resolve to final path;
- source/test/document verifiers should flag legacy path references;
- no compatibility duplicate folders are maintained.

## 8. Final state

```text
PARALLEL ACTIVE MANUALS   PROHIBITED
CANONICAL AUTHORITY       Documents/
REFERENCE BASELINE        GoldSwingTraderAI
CURRENT FOLDER SCHEME     01–08
HISTORICAL REVISIONS      Git history
```
