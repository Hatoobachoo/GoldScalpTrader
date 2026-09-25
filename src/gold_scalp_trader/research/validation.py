"""Chronological research validation and walk-forward boundaries.

These helpers prevent overlapping validation/holdout windows and make final
holdout consumption explicit. They never select or promote production policy.
"""
from __future__ import annotations

from dataclasses import dataclass


def non_overlapping(train_end: int, validation_start: int, validation_end: int, holdout_start: int) -> bool:
    return train_end <= validation_start < validation_end <= holdout_start


@dataclass(frozen=True, slots=True)
class ValidationWindows:
    train_start: int
    train_end: int
    validation_start: int
    validation_end: int
    holdout_start: int
    holdout_end: int

    def __post_init__(self) -> None:
        if not (self.train_start < self.train_end <= self.validation_start < self.validation_end <= self.holdout_start < self.holdout_end):
            raise ValueError("research windows must be chronological and non-overlapping")


@dataclass(frozen=True, slots=True)
class WalkForwardFold:
    fold: int
    train_start: int
    train_end: int
    validation_start: int
    validation_end: int

    def __post_init__(self) -> None:
        if self.fold < 0:
            raise ValueError("fold cannot be negative")
        if not (0 <= self.train_start < self.train_end <= self.validation_start < self.validation_end):
            raise ValueError("walk-forward fold must be chronological and non-overlapping")


def walk_forward_folds(
    *,
    development_count: int,
    train_size: int,
    validation_size: int,
    step_size: int | None = None,
    expanding_train: bool = True,
) -> tuple[WalkForwardFold, ...]:
    """Build fixed chronological development/validation folds.

    `development_count` must exclude the untouched final holdout. No fold can
    reach beyond this development region.
    """
    if development_count <= 0 or train_size <= 0 or validation_size <= 0:
        raise ValueError("development_count/train_size/validation_size must be positive")
    step = validation_size if step_size is None else step_size
    if step <= 0:
        raise ValueError("step_size must be positive")
    if train_size + validation_size > development_count:
        raise ValueError("insufficient development data for one walk-forward fold")

    folds: list[WalkForwardFold] = []
    validation_start = train_size
    fold_index = 0
    while validation_start + validation_size <= development_count:
        train_end = validation_start
        train_start = 0 if expanding_train else max(0, train_end - train_size)
        folds.append(WalkForwardFold(fold_index, train_start, train_end, validation_start, validation_start + validation_size))
        fold_index += 1
        validation_start += step
    return tuple(folds)


@dataclass(frozen=True, slots=True)
class HoldoutUse:
    candidate_fingerprint: str
    dataset_sha256: str
    consumed: bool = False


def consume_holdout(state: HoldoutUse) -> HoldoutUse:
    if state.consumed:
        raise ValueError("final holdout is one-shot for this candidate/dataset identity")
    if not state.candidate_fingerprint or not state.dataset_sha256:
        raise ValueError("candidate and dataset identity are required")
    return HoldoutUse(state.candidate_fingerprint, state.dataset_sha256, True)
