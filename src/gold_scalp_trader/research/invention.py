"""Declarative autonomous strategy invention; never executable generated code."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1

from .promotion import Candidate

ALLOWED_PRIMITIVES = {
    "STRUCTURE_TREND", "STRUCTURE_BREAK", "MSS_SHIFT", "CANDLE_REJECTION",
    "DISPLACEMENT", "COMPRESSION", "TECHNICAL_LOCATION", "LIQUIDITY_SWEEP",
    "FVG", "ORDER_BLOCK", "EMA_FLOW", "RSI_MOMENTUM", "ATR_VOLATILITY",
    "SESSION_CONTEXT", "NEWS_CONTEXT", "TARGET_PATH", "M5_SETUP",
    "M1_ENTRY_TIMING", "EXECUTABLE_COST", "MANAGEMENT_EFFICIENCY",
}
ALLOWED_CANDIDATE_TYPES = {
    "VARIANT", "NEW_FAMILY", "ENTRY_POLICY", "EXIT_POLICY", "QUALITY_POLICY",
    "REGIME_POLICY", "MODEL_ASSISTED_POLICY",
}


@dataclass(frozen=True, slots=True)
class Recipe:
    required: tuple[str, ...]
    supportive: tuple[str, ...]
    direction_model: str
    timing_model: str
    candidate_type: str = "NEW_FAMILY"
    parent_family: str | None = None
    hypothesis: str = ""
    version: str = "1"

    def __post_init__(self) -> None:
        unknown = (set(self.required) | set(self.supportive)) - ALLOWED_PRIMITIVES
        if unknown:
            raise ValueError(f"unknown primitives: {sorted(unknown)}")
        if self.candidate_type not in ALLOWED_CANDIDATE_TYPES:
            raise ValueError(f"unsupported candidate type: {self.candidate_type}")
        if not self.direction_model.strip() or not self.timing_model.strip():
            raise ValueError("direction_model and timing_model are required")
        if not self.version.strip():
            raise ValueError("candidate recipe version is required")


def invent(recipe: Recipe, source_episode_ids: tuple[str, ...]) -> Candidate:
    if not source_episode_ids:
        raise ValueError("candidate invention requires source episode identity")
    sources = tuple(dict.fromkeys(str(x) for x in source_episode_ids if str(x)))
    if not sources:
        raise ValueError("candidate invention requires source episode identity")
    semantics = {
        "version": recipe.version,
        "candidate_type": recipe.candidate_type,
        "parent_family": recipe.parent_family,
        "hypothesis": recipe.hypothesis,
        "required": recipe.required,
        "supportive": recipe.supportive,
        "direction_model": recipe.direction_model,
        "timing_model": recipe.timing_model,
        "sources": sources,
    }
    raw = "|".join(
        (
            recipe.version,
            recipe.candidate_type,
            recipe.parent_family or "NONE",
            recipe.hypothesis,
            *recipe.required,
            *recipe.supportive,
            *sources,
            recipe.direction_model,
            recipe.timing_model,
        )
    )
    candidate_id = f"CAND-{sha1(raw.encode()).hexdigest()[:12]}"
    return Candidate(candidate_id, recipe.candidate_type, semantics)


__all__ = ["ALLOWED_CANDIDATE_TYPES", "ALLOWED_PRIMITIVES", "Recipe", "invent"]
