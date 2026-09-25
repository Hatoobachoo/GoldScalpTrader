"""Chronological research validation boundaries.

These helpers prevent overlapping validation/holdout windows and make the
one-shot holdout consumption explicit. They never promote production policy.
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
