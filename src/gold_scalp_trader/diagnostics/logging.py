"""Structured logging helpers with intentionally small surface area."""
from __future__ import annotations
import logging


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    return logging.getLogger("gold_scalp_trader")
