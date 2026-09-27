"""Static document/code contract guard for the GoldScalpTrader offline release.

This verifier deliberately checks architectural wiring that unit tests can miss:
sole canonical DEMO runtime, no caller Session override, durable Risk-day sizing,
research-only shadow lifecycle, verified stage-proof issuance, sole MT5 writer,
and frozen policy constants. It never claims connected Exness proof.
"""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "gold_scalp_trader"
DOCS = ROOT / "Documents"
CATALOG = DOCS / "07-engineering" / "FILE_AND_TEST_CATALOG.md"

EXPECTED_DOC_COUNTS = {
    "01-foundation": 5,
    "02-market-intelligence": 7,
    "03-trading-decisions": 7,
    "04-risk-execution": 6,
    "05-research-learning": 7,
    "06-operator": 3,
    "07-engineering": 14,
    "08-governance": 8,
}

REQUIRED_SOURCE_PATHS = (
    "config/settings.py", "domain/enums.py", "domain/ids.py", "domain/market.py", "domain/models.py",
    "market_data/account_mode.py", "market_data/mt5_reader.py", "market_data/activity.py", "market_data/snapshot.py",
    "intelligence/candle_structure.py", "intelligence/indicators.py", "intelligence/technical.py",
    "intelligence/liquidity.py", "intelligence/confluence.py", "intelligence/session.py", "intelligence/news.py",
    "intelligence/snapshot.py", "strategies/floor.py", "strategies/setup_detector.py", "strategies/isolation.py",
    "decisions/fusion.py", "decisions/opportunity.py", "decisions/timing.py", "decisions/family_trade_plan.py",
    "decisions/trade_plan.py", "decisions/executable_quality.py", "risk/engine.py", "risk/state.py",
    "risk/runtime.py", "risk/permissions.py", "execution/models.py", "execution/checks.py", "execution/gate.py",
    "execution/intent_store.py", "execution/service.py", "execution/mt5_writer.py", "execution/reconcile.py",
    "execution/controller.py", "management/models.py", "management/manager.py", "management/execution.py",
    "management/closure.py", "management/store.py", "persistence/store.py", "persistence/checkpoint.py",
    "research/learning.py", "research/live_learning.py", "research/timing_learning.py", "research/runtime_evidence.py",
    "research/outcomes.py", "research/shadow_runtime.py", "research/candidate_registry.py",
    "research/stage_orchestrator.py", "research/replay.py", "research/management_replay.py",
    "research/session_history.py", "research/stress.py", "research/validation.py", "research/evidence.py",
    "research/packages.py", "research/metrics.py", "research/ablation.py", "research/discovery.py",
    "research/invention.py", "research/promotion.py", "operator/presentation.py", "operator/terminal_dashboard.py",
    "app/runtime.py", "app/runtime_core.py", "app/session_authority.py", "app/opportunity_lifecycle.py",
    "app/cycle.py", "app/demo_runner.py",
)

CRITICAL_TESTS = (
    "tests/test_cycle_no_forcing.py", "tests/test_strategy_isolation.py", "tests/test_decision_pipeline.py",
    "tests/test_risk_profiles.py", "tests/test_risk_runtime_state.py", "tests/test_session_runtime_authority.py",
    "tests/test_guarded_demo_runtime.py", "tests/test_execution_intent.py", "tests/test_gate.py",
    "tests/test_controller.py", "tests/test_management_lifecycle.py", "tests/test_live_learning_pipeline.py",
    "tests/test_runtime_research_evidence.py", "tests/test_shadow_runtime.py",
    "tests/test_research_runtime_isolation.py", "tests/test_candidate_registry.py",
    "tests/test_research_integrity.py", "tests/test_full_checkpoint.py",
)

ANALYTICAL_NO_BROKER_DIRS = (
    SRC / "intelligence", SRC / "strategies", SRC / "risk", SRC / "research",
    SRC / "operator", SRC / "diagnostics", ROOT / "graphical_dashboard",
)
FORBIDDEN_IMPORT_FRAGMENTS = ("MetaTrader5", "execution.mt5_writer")
STALE_POLICY_TERMS = ("NEWS_BLACKOUT", "POST_NEWS_WARMUP", "M1 diagnostic-only", "M1 diagnostic only")

CATALOG_REQUIRED_FRAGMENTS = (
    "**Version:** 2.6-institutional-scalp-implementation",
    "app/session_news.py", "app/session_authority.py", "tests/test_session_runtime_authority.py",
    "app/opportunity_lifecycle.py", "tests/test_opportunity_lifecycle.py", "app/runtime_core.py",
    "research/timing_learning.py", "tests/test_timing_learning_lineage.py",
    "research/runtime_evidence.py", "tests/test_runtime_research_evidence.py",
    "research/shadow_runtime.py", "tests/test_shadow_runtime.py",
    "research/stage_orchestrator.py", "research/candidate_registry.py", "tests/test_candidate_registry.py",
    "verified valid Session OPEN", "News health                 → never a hard-trading permission",
    "verified full-close queue item", "consume queue only after durable save",
    "runtime activation remains separate from candidate registry stage",
    "REAL = hard-disabled", "Connected DEMO proof — still external",
)


def _fail(errors: list[str], message: str) -> None:
    errors.append(message)


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _function(tree: ast.Module, name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    return next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name), None)


def _literal_assignment(tree: ast.Module, name: str):
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == name for target in targets):
                if node.value is None:
                    return None
                return ast.literal_eval(node.value)
    raise KeyError(name)


def check_documents(errors: list[str]) -> None:
    for folder, expected in EXPECTED_DOC_COUNTS.items():
        path = DOCS / folder
        actual = len(list(path.glob("*.md"))) if path.is_dir() else -1
        if actual != expected:
            _fail(errors, f"document count {folder}: expected {expected}, got {actual}")
    total = len(list(DOCS.rglob("*.md")))
    if total != 66:
        _fail(errors, f"document total: expected 66, got {total}")


def check_required_paths(errors: list[str]) -> None:
    for rel in REQUIRED_SOURCE_PATHS:
        if not (SRC / rel).is_file():
            _fail(errors, f"missing canonical source owner: src/gold_scalp_trader/{rel}")
    for rel in CRITICAL_TESTS:
        if not (ROOT / rel).is_file():
            _fail(errors, f"missing critical regression proof: {rel}")


def check_catalog(errors: list[str]) -> None:
    if not CATALOG.is_file():
        _fail(errors, "missing FILE_AND_TEST_CATALOG.md")
        return
    text = CATALOG.read_text(encoding="utf-8")
    for fragment in CATALOG_REQUIRED_FRAGMENTS:
        if fragment not in text:
            _fail(errors, f"implemented proof disappeared from engineering catalog: {fragment}")


def check_frozen_policy(errors: list[str]) -> None:
    path = SRC / "config" / "settings.py"
    text = path.read_text(encoding="utf-8")
    try:
        real_enabled = _literal_assignment(_tree(path), "REAL_RELEASE_ENABLED")
    except (KeyError, ValueError) as exc:
        _fail(errors, f"REAL_RELEASE_ENABLED cannot be verified: {exc}")
    else:
        if real_enabled is not False:
            _fail(errors, "REAL_RELEASE_ENABLED must remain False")
    for expected in (
        '"SMALL": RiskBand(3.0, 4.5, 6.5, 7.0, 12.0)',
        '"MEDIUM": RiskBand(2.0, 3.0, 4.5, 5.0, 9.0)',
        '"NORMAL": RiskBand(1.0, 2.0, 3.5, 4.0, 7.0)',
        "max_open_positions: int = 1", "max_consecutive_losses: int = 3",
        "consecutive_loss_cooldown_minutes: int = 30", "aggressive_small_account: bool = False",
        "manual_daily_loss_reset_enabled: bool = False",
    ):
        if expected not in text:
            _fail(errors, f"preserved policy changed/missing: {expected}")


def check_broker_boundaries(errors: list[str]) -> None:
    for directory in ANALYTICAL_NO_BROKER_DIRS:
        for path in directory.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            for fragment in FORBIDDEN_IMPORT_FRAGMENTS:
                if fragment in text:
                    _fail(errors, f"forbidden broker dependency in {path.relative_to(ROOT)}: {fragment}")
            if "order_send(" in text or "order_send (" in text:
                _fail(errors, f"raw order_send outside sole writer: {path.relative_to(ROOT)}")
    if "order_send" not in (SRC / "execution" / "mt5_writer.py").read_text(encoding="utf-8"):
        _fail(errors, "sole MT5 writer lost raw order_send boundary")


def check_runtime_authorities(errors: list[str]) -> None:
    runtime_path = SRC / "app" / "runtime.py"
    core_path = SRC / "app" / "runtime_core.py"
    runtime_tree = _tree(runtime_path)
    core_tree = _tree(core_path)
    guarded = _function(runtime_tree, "run_guarded_demo_cycle")
    if guarded is None:
        _fail(errors, "canonical run_guarded_demo_cycle missing")
    else:
        args = {arg.arg for arg in (*guarded.args.args, *guarded.args.kwonlyargs)}
        if "market_open" in args:
            _fail(errors, "canonical runtime exposes caller Session override market_open")
    if _function(core_tree, "run_guarded_demo_cycle") is not None:
        _fail(errors, "runtime_core exposes duplicate full guarded execution path")

    runtime = runtime_path.read_text(encoding="utf-8")
    for required in (
        "prepare_risk_authority(",
        "day_start_equity=authority.state.day_start_equity",
        "session_action_allowed(provider, action) and broker_allowed is True",
    ):
        if required not in runtime:
            _fail(errors, f"canonical runtime authority wiring missing: {required}")

    core = core_path.read_text(encoding="utf-8")
    if "authority_allowed: bool" not in core or "effective_permission = authority_allowed and broker_allowed is True" not in core:
        _fail(errors, "managed runtime mechanics are not bound to canonical Session permission")


def check_research_governance(errors: list[str]) -> None:
    shadow = (SRC / "research" / "shadow_runtime.py").read_text(encoding="utf-8")
    for forbidden in ("execution.mt5_writer", "execution.gate", "risk.engine", "order_send("):
        if forbidden in shadow:
            _fail(errors, f"shadow lifecycle gained forbidden authority: {forbidden}")
    for required in ("SHADOW_ONLY", "TERMINAL_NS", "evaluate_counterfactual_path", "broker_authority"):
        if required not in shadow:
            _fail(errors, f"shadow lifecycle invariant missing: {required}")

    registry = (SRC / "research" / "candidate_registry.py").read_text(encoding="utf-8")
    orchestrator = (SRC / "research" / "stage_orchestrator.py").read_text(encoding="utf-8")
    if "def record_stage_evidence(" in registry:
        _fail(errors, "candidate registry exposes arbitrary public stage PASS issuer")
    if "VERIFIED_STAGE_PACKAGE_V1" not in registry or "package_manifest_sha256" not in registry:
        _fail(errors, "candidate registry is not bound to verified stage packages")
    for required in ("verify_evidence_package", "required_checks", "candidate_fingerprint", "passed"):
        if required not in orchestrator:
            _fail(errors, f"stage proof orchestrator invariant missing: {required}")
    if "runtime_activation_allowed" not in registry or "return False" not in registry:
        _fail(errors, "candidate registry can no longer prove zero runtime activation authority")

    runner = (SRC / "app" / "demo_runner.py").read_text(encoding="utf-8")
    if "_record_research_best_effort" not in runner or "record_shadow_runtime" not in runner:
        _fail(errors, "runtime research/shadow evidence is not isolated/wired")


def check_no_legacy_policy_code(errors: list[str]) -> None:
    for path in SRC.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for term in STALE_POLICY_TERMS:
            if term in text:
                _fail(errors, f"legacy policy term in {path.relative_to(ROOT)}: {term}")


def main() -> int:
    errors: list[str] = []
    check_documents(errors)
    check_required_paths(errors)
    check_catalog(errors)
    check_frozen_policy(errors)
    check_broker_boundaries(errors)
    check_runtime_authorities(errors)
    check_research_governance(errors)
    check_no_legacy_policy_code(errors)

    print("DOCUMENT / CODE CONTRACT SYNC AUDIT")
    if errors:
        for error in errors:
            print(f"  FAIL  {error}")
        print(f"CONTRACT SYNC: FAIL ({len(errors)} issue(s))")
        return 1

    print("  PASS  66-document topology")
    print("  PASS  canonical source / critical-test ownership paths")
    print("  PASS  preserved Risk / cooldown / REAL-disable policy")
    print("  PASS  sole canonical DEMO runtime; no caller Session override")
    print("  PASS  durable UTC Risk-day authority wired into live OPEN sizing")
    print("  PASS  Session hard / News soft authority boundaries")
    print("  PASS  sole-writer / no-broker analytical boundaries")
    print("  PASS  automatic causal SHADOW_ONLY outcome lifecycle")
    print("  PASS  verified immutable stage-proof issuance; no direct runtime activation")
    print("  PASS  research evidence failures isolated from broker-cycle authority")
    print("CONTRACT SYNC: PASS")
    print("CONNECTED DEMO FACTS: NOT PROVEN BY THIS STATIC AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
