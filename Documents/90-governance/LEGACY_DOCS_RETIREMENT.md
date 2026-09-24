# GoldScalpTrader — Legacy Docs Retirement

**Status:** DRAFT GOVERNANCE RECORD — NO PARALLEL LEGACY TREE EXISTS
**Version:** 0.1-no-legacy-authority
**Authority:** Canonical record preventing creation of a second competing documentation tree.

## 1. Decision

GoldScalpTrader currently has no historical lowercase `docs/` product manual that needs migration/retirement.

The current rule is simply:

```text
Documents/       = only current documentation authority
lowercase docs/  = must not be created as a competing active manual
Git history       = historical source for prior revisions of canonical files
```

This differs from GoldSwingTraderAI, where an actual old lowercase tree was inspected and retired.

## 2. Why this file still exists

The user requires the complete reference-equivalent documentation topology. This filename also protects against a future contributor recreating a parallel manual by habit.

It records a truthful state rather than fabricating a retirement event that never occurred.

## 3. If legacy material appears later

Do not immediately copy it into active truth.

Use this process:

```text
inventory legacy material
→ compare against current canonical Documents/
→ preserve useful rationale/constraints
→ record supersession/relocation
→ update Preservation Ledger / Comparison / Coverage Matrix
→ obtain explicit governance approval if deletion/retirement is consequential
→ keep one active authority only
```

## 4. Reference GoldSwingTraderAI material

GoldSwingTraderAI `Documents/` is a **design reference/preservation source**, not a lowercase legacy tree inside this repository.

Its useful architecture is adapted through `PRESERVATION_LEDGER.md` and `DOCUMENTATION_COMPARISON.md`.

Reference text never becomes a second active authority after the GoldScalpTrader topic contract exists.

## 5. Prohibited state

Do not maintain:

```text
Documents/ with rule A
+ docs/ with rule B
+ README/prompt with rule C
```

Top-level project README and build prompts summarize canonical Documents and may not override them.

## 6. Current state

```text
RETIREMENT ACTION: NOT APPLICABLE
PARALLEL LEGACY TREE: ABSENT
CANONICAL AUTHORITY: Documents/
```

If this topology changes, update this governance record in the same affected-graph packet.
