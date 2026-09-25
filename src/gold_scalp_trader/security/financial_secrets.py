"""Best-effort secret-pattern detection for local artifacts/logging.

This module detects obvious authority-bearing values; it is not a credential
store and never returns detected secret text in error messages.
"""
from __future__ import annotations
import re

_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(password|api[_-]?key|secret|token)\s*[=:]\s*[^\s]+"),
)


def contains_probable_secret(text: str) -> bool:
    return any(pattern.search(text) is not None for pattern in _PATTERNS)


def redact(text: str) -> str:
    result = text
    for pattern in _PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result
