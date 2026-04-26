"""URL validation helpers."""

from __future__ import annotations

import re

_LOCAL_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p) for p in (
        r"localhost",
        r"127\.0\.0\.1",
        r"192\.168\.",
        r"\b10\.",
        r"172\.(1[6-9]|2[0-9]|3[0-1])\.",
    )
)


def is_local_url(url: str) -> bool:
    """Return ``True`` if ``url`` points to a local or private network host."""
    if not url:
        return False
    return any(pattern.search(url) for pattern in _LOCAL_PATTERNS)
