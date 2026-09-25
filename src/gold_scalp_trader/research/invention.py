"""Declarative autonomous strategy invention; never executable generated code."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha1
from .promotion import Candidate
ALLOWED_PRIMITIVES={"STRUCTURE_TREND","STRUCTURE_BREAK","MSS_SHIFT","CANDLE_REJECTION","DISPLACEMENT","COMPRESSION","TECHNICAL_LOCATION","LIQUIDITY_SWEEP","FVG","ORDER_BLOCK","EMA_FLOW","RSI_MOMENTUM","ATR_VOLATILITY","SESSION_CONTEXT","NEWS_CONTEXT","TARGET_PATH","M5_SETUP","M1_ENTRY_TIMING","EXECUTABLE_COST","MANAGEMENT_EFFICIENCY"}
@dataclass(frozen=True,slots=True)
class Recipe:
    required:tuple[str,...]; supportive:tuple[str,...]; direction_model:str; timing_model:str
def invent(recipe:Recipe,source_episode_ids:tuple[str,...])->Candidate:
    unknown=(set(recipe.required)|set(recipe.supportive))-ALLOWED_PRIMITIVES
    if unknown:raise ValueError(f"unknown primitives: {sorted(unknown)}")
    raw="|".join((*recipe.required,*recipe.supportive,*source_episode_ids,recipe.direction_model,recipe.timing_model)); cid=f"CAND-{sha1(raw.encode()).hexdigest()[:12]}"
    return Candidate(cid,"NEW_FAMILY",{"required":recipe.required,"supportive":recipe.supportive,"direction_model":recipe.direction_model,"timing_model":recipe.timing_model,"sources":source_episode_ids})
