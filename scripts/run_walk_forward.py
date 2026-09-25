"""Build an auditable chronological walk-forward plan for a verified dataset.

This local research tool never connects to MT5 and never changes production
policy. Strategy/candidate evaluation consumes these folds through the research
replay/evidence pipeline.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from gold_scalp_trader.research.datasets import build_dataset_identity
from gold_scalp_trader.research.validation import walk_forward_folds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--development-count", type=int, required=True, help="rows/bars available before untouched final holdout")
    parser.add_argument("--train-size", type=int, required=True)
    parser.add_argument("--validation-size", type=int, required=True)
    parser.add_argument("--step-size", type=int)
    parser.add_argument("--rolling-train", action="store_true", help="use fixed rolling train window instead of expanding window")
    parser.add_argument("--dataset-file", action="append", default=[])
    parser.add_argument("--source", default="unspecified")
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument("--version", default="v1")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    folds = walk_forward_folds(
        development_count=args.development_count,
        train_size=args.train_size,
        validation_size=args.validation_size,
        step_size=args.step_size,
        expanding_train=not args.rolling_train,
    )
    payload: dict[str, object] = {
        "development_count": args.development_count,
        "train_size": args.train_size,
        "validation_size": args.validation_size,
        "step_size": args.validation_size if args.step_size is None else args.step_size,
        "expanding_train": not args.rolling_train,
        "folds": [asdict(fold) for fold in folds],
        "broker_authority": "NONE",
        "production_promotion": "NOT_PERMITTED_BY_THIS_TOOL",
    }
    if args.dataset_file:
        identity = build_dataset_identity(
            source=args.source,
            symbol=args.symbol,
            version=args.version,
            paths=[Path(path) for path in args.dataset_file],
        )
        payload["dataset_identity"] = asdict(identity)

    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite existing walk-forward plan: {args.output}")
        args.output.write_text(text, encoding="utf-8")
        print(args.output)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
