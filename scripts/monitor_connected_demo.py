"""Continuously accumulate read-only connected DEMO certification evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time

from certify_connected_demo import collect
from gold_scalp_trader.diagnostics.connected_demo import aggregate_connected_demo_reports

UTC = timezone.utc


def _atomic_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temp.replace(path)


def _session_text(report: dict[str, object]) -> str:
    session = report.get("session")
    if not isinstance(session, dict):
        return "session=UNKNOWN schedule_verified=False tradeable=None"
    return (
        f"session={session.get('state', 'UNKNOWN')} "
        f"schedule_verified={session.get('schedule_verified')} "
        f"tradeable={session.get('tradeable')}"
    )


def _research_text(report: dict[str, object]) -> str:
    research = report.get("runtime_research")
    if not isinstance(research, dict):
        return "timing=0 management=0 shadow=0"
    return (
        f"timing={research.get('timing_samples', 0)} "
        f"management={research.get('management_samples', 0)} "
        f"shadow={research.get('shadow_samples', 0)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("runtime/evidence"))
    parser.add_argument(
        "--operator-evidence-dir",
        type=Path,
        default=Path("runtime/evidence/operator-drills"),
    )
    parser.add_argument("--interval-seconds", type=float, default=60.0)
    parser.add_argument("--max-samples", type=int, default=360)
    parser.add_argument("--stop-on-core-lifecycle", action="store_true")
    parser.add_argument("--fail-fast", action="store_true")
    args = parser.parse_args()

    if args.interval_seconds < 5.0:
        raise SystemExit("--interval-seconds must be at least 5 seconds")
    if args.max_samples < 1:
        raise SystemExit("--max-samples must be at least 1")

    run_dir = args.output_dir / f"connected-demo-watch-{datetime.now(tz=UTC).strftime('%Y%m%dT%H%M%SZ')}"
    run_dir.mkdir(parents=True, exist_ok=False)
    reports: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []

    print("GoldScalpTrader — Connected DEMO evidence monitor")
    print("BROKER WRITES BY THIS MONITOR: NONE")
    print(f"Output: {run_dir}")
    print(f"Operator drill evidence: {args.operator_evidence_dir}")

    for index in range(1, args.max_samples + 1):
        try:
            report = collect(args.operator_evidence_dir)
            reports.append(report)
            _atomic_json(run_dir / f"sample-{index:04d}.json", report)
            summary = aggregate_connected_demo_reports(reports)
            summary["monitor_errors"] = list(errors)
            _atomic_json(run_dir / "summary.json", summary)
            print(
                f"sample={index} "
                f"core={summary['core_demo_lifecycle_observed']} "
                f"full={summary['full_connected_certification']} "
                f"spread={report['quote']['spread']} "
                f"quote_age={report['quote']['age_seconds']:.3f}s "
                f"{_session_text(report)} "
                f"{_research_text(report)}"
            )
            session = report.get("session")
            if isinstance(session, dict) and session.get("reason"):
                print(f"  session_reason={session['reason']}")
            if args.stop_on_core_lifecycle and summary["core_demo_lifecycle_observed"] == "PASS":
                print("Core DEMO lifecycle evidence observed. External/manual drills may still be pending.")
                break
        except KeyboardInterrupt:
            print("Stopped by operator.")
            break
        except Exception as exc:
            event = {
                "captured_at_utc": datetime.now(tz=UTC).isoformat(),
                "error_type": type(exc).__name__,
                "message": str(exc),
            }
            errors.append(event)
            _atomic_json(run_dir / "errors.json", {"errors": errors})
            print(f"sample={index} ERROR {type(exc).__name__}: {exc}")
            if args.fail_fast:
                return 2
        if index < args.max_samples:
            try:
                time.sleep(args.interval_seconds)
            except KeyboardInterrupt:
                print("Stopped by operator.")
                break

    if reports:
        summary = aggregate_connected_demo_reports(reports)
        summary["monitor_errors"] = list(errors)
        _atomic_json(run_dir / "summary.json", summary)
        print(f"Summary: {run_dir / 'summary.json'}")
        print(f"CORE DEMO LIFECYCLE: {summary['core_demo_lifecycle_observed']}")
        print(f"FULL CONNECTED CERTIFICATION: {summary['full_connected_certification']}")
        return 0

    print("No valid connected DEMO sample was collected.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
