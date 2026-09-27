from types import SimpleNamespace

from gold_scalp_trader.app import demo_runner
from gold_scalp_trader.persistence.store import StateStore


def test_research_recording_failure_cannot_reclassify_runtime_cycle(monkeypatch):
    calls = []

    def timing(store, result):
        calls.append("timing")
        raise RuntimeError("timing evidence disk fault")

    def management(store, result):
        calls.append("management")
        return ("ok",)

    def shadow(store, result):
        calls.append("shadow")
        raise ValueError("shadow evidence fault")

    monkeypatch.setattr(demo_runner, "record_runtime_timing", timing)
    monkeypatch.setattr(demo_runner, "record_runtime_research", management)
    monkeypatch.setattr(demo_runner, "record_shadow_runtime", shadow)

    result = SimpleNamespace(wrote_broker=True)
    failures = demo_runner._record_research_best_effort(StateStore(), result)

    assert calls == ["timing", "management", "shadow"]
    assert failures == ("TIMING:RuntimeError", "SHADOW_OUTCOME:ValueError")
    assert result.wrote_broker is True
