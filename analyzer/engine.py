"""Heuristic analysis engine.

This module evaluates URLs against curated domain lists and a lexicon of
trigger phrases. It is rule-based — there is no machine learning.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Protocol

from analyzer.constants import (
    RESTRICTED_BLACKLIST,
    RUSSIAN_STATE_MEDIA_BLACKLIST,
    SATIRE_BLACKLIST,
    TRIGGER_PHRASES,
)


class DomainStatus(str, Enum):
    """Classification of a URL's domain reputation."""

    SATIRE = "satire"
    RESTRICTED = "restricted"
    CLEAN = "clean"


@dataclass(frozen=True)
class AnalysisResult:
    """Outcome of running heuristic analysis on article text."""

    is_misinfo: int
    confidence: float
    hit_count: int


class ArticleFetcher(Protocol):
    """Anything that can turn a URL into ``(title, text)`` for testing."""

    def __call__(self, url: str) -> tuple[str, str]:  # pragma: no cover - protocol
        ...


def _default_fetcher(url: str) -> tuple[str, str]:
    """Real fetcher backed by ``newspaper3k``.

    Imported lazily so that unit tests don't pay the import cost and don't
    need network access.
    """
    from newspaper import Article  # local import keeps tests light

    article = Article(url)
    article.download()
    article.parse()
    if not article.text:
        raise ValueError("empty")
    return article.title, article.text


class MisinformationEngine:
    """Evaluates content against domain reputation and heuristic risk patterns."""

    def __init__(
        self,
        *,
        satire_domains: Iterable[str] | None = None,
        restricted_domains: Iterable[str] | None = None,
        trigger_phrases: Iterable[str] | None = None,
        fetcher: ArticleFetcher | None = None,
    ) -> None:
        self.satire_domains = frozenset(satire_domains or SATIRE_BLACKLIST)
        self.restricted_domains = frozenset(
            restricted_domains
            or RESTRICTED_BLACKLIST.union(RUSSIAN_STATE_MEDIA_BLACKLIST)
        )
        self.trigger_phrases = tuple(trigger_phrases or TRIGGER_PHRASES)
        self._fetcher: ArticleFetcher = fetcher or _default_fetcher

    def check_domain_type(self, url: str) -> DomainStatus:
        """Classify the URL by its domain reputation."""
        url_lower = url.lower()
        if any(domain in url_lower for domain in self.satire_domains):
            return DomainStatus.SATIRE
        if any(domain in url_lower for domain in self.restricted_domains):
            return DomainStatus.RESTRICTED
        return DomainStatus.CLEAN

    def extract_text(self, url: str) -> tuple[str, str]:
        """Fetch and parse article content, returning ``(title, text)``."""
        return self._fetcher(url)

    def analyze(self, text: str) -> AnalysisResult:
        """Run heuristic analysis on article text.

        Scoring (rule-based thresholds, **not** statistical probabilities):

        * 0 hits  -> cleared, score 0.95
        * 1 hit   -> flagged,  score 0.40 (low confidence)
        * 2 hits  -> flagged,  score 0.65
        * 3+ hits -> flagged,  score 0.85
        """
        if not text or not text.strip():
            raise ValueError("empty")

        text_lower = text.lower()
        hit_count = sum(1 for phrase in self.trigger_phrases if phrase in text_lower)

        if hit_count == 0:
            return AnalysisResult(0, 0.95, 0)
        if hit_count == 1:
            return AnalysisResult(1, 0.40, 1)
        if hit_count == 2:
            return AnalysisResult(1, 0.65, 2)
        return AnalysisResult(1, 0.85, hit_count)
