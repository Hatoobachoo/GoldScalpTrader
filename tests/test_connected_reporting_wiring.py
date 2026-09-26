from __future__ import annotations

from pathlib import Path


def test_connected_reporting_wires_session_and_runtime_learning_evidence() -> None:
    root = Path(__file__).resolve().parents[1]
    certify = (root / "scripts" / "certify_connected_demo.py").read_text(encoding="utf-8")
    monitor = (root / "scripts" / "monitor_connected_demo.py").read_text(encoding="utf-8")
    report = (root / "scripts" / "report_demo_learning_evidence.py").read_text(encoding="utf-8")

    assert "resolve_session" in certify
    assert "summarize_local_research" in certify
    assert '"session": session' in certify
    assert '"runtime_research": local_research' in certify
    assert "_session_text" in monitor
    assert "_research_text" in monitor
    assert "session_reason=" in monitor
    assert "summarize_local_research" in report
    assert not (root / "scripts" / "certify_connected_demo.py.tmp").exists()
