"""Ablation helpers for measuring marginal research contribution.

Ablation is descriptive research evidence only. It must not turn an optional
indicator/confluence primitive into a live universal veto.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping


@dataclass(frozen=True, slots=True)
class AblationResult:
    feature: str
    full_net_r: float
    without_feature_net_r: float
    marginal_net_r: float
    full_opportunity_recall: float | None = None
    without_feature_opportunity_recall: float | None = None
    recall_delta: float | None = None


def marginal_net_r(full_net_r: float, without_feature_net_r: float) -> float:
    if not isfinite(float(full_net_r)) or not isfinite(float(without_feature_net_r)):
        raise ValueError("Net R values must be finite")
    return float(full_net_r) - float(without_feature_net_r)


def compare_feature(
    feature: str,
    *,
    full_net_r: float,
    without_feature_net_r: float,
    full_opportunity_recall: float | None = None,
    without_feature_opportunity_recall: float | None = None,
) -> AblationResult:
    if not feature.strip():
        raise ValueError("feature is required")
    recall_delta: float | None = None
    if (full_opportunity_recall is None) != (without_feature_opportunity_recall is None):
        raise ValueError("both recall values must be supplied together")
    if full_opportunity_recall is not None and without_feature_opportunity_recall is not None:
        for value in (full_opportunity_recall, without_feature_opportunity_recall):
            if not isfinite(float(value)) or not 0.0 <= float(value) <= 1.0:
                raise ValueError("opportunity recall must be within 0..1")
        recall_delta = float(full_opportunity_recall) - float(without_feature_opportunity_recall)
    return AblationResult(
        feature=feature.strip(),
        full_net_r=float(full_net_r),
        without_feature_net_r=float(without_feature_net_r),
        marginal_net_r=marginal_net_r(full_net_r, without_feature_net_r),
        full_opportunity_recall=None if full_opportunity_recall is None else float(full_opportunity_recall),
        without_feature_opportunity_recall=None if without_feature_opportunity_recall is None else float(without_feature_opportunity_recall),
        recall_delta=recall_delta,
    )


def rank_by_marginal_net_r(results: Mapping[str, AblationResult] | tuple[AblationResult, ...]) -> tuple[AblationResult, ...]:
    values = tuple(results.values()) if isinstance(results, Mapping) else tuple(results)
    return tuple(sorted(values, key=lambda row: (-row.marginal_net_r, row.feature)))
