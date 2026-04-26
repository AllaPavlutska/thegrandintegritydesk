"""Tests for ``analyzer.engine``."""

from __future__ import annotations

import pytest

from analyzer.engine import AnalysisResult, DomainStatus, MisinformationEngine


@pytest.fixture()
def engine() -> MisinformationEngine:
    return MisinformationEngine()


# ---------------------------------------------------------------------------
# Domain classification
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "url",
    [
        "https://theonion.com/article/whatever",
        "https://www.clickhole.com/x",
        "https://der-postillon.com/y",
    ],
)
def test_satire_domains_are_classified_satire(
    engine: MisinformationEngine, url: str
) -> None:
    assert engine.check_domain_type(url) is DomainStatus.SATIRE


@pytest.mark.parametrize(
    "url",
    [
        "https://infowars.com/x",
        "https://www.naturalnews.com/y",
        "https://rt.com/news/123",
        "https://news.tass.com/abc",
    ],
)
def test_restricted_domains_are_classified_restricted(
    engine: MisinformationEngine, url: str
) -> None:
    assert engine.check_domain_type(url) is DomainStatus.RESTRICTED


@pytest.mark.parametrize(
    "url",
    [
        "https://www.nytimes.com/article",
        "https://example.com/page",
        "https://bbc.co.uk/news",
    ],
)
def test_clean_domains_are_classified_clean(
    engine: MisinformationEngine, url: str
) -> None:
    assert engine.check_domain_type(url) is DomainStatus.CLEAN


def test_satire_takes_precedence_over_restricted() -> None:
    eng = MisinformationEngine(
        satire_domains={"shared.com"},
        restricted_domains={"shared.com"},
    )
    assert eng.check_domain_type("https://shared.com/x") is DomainStatus.SATIRE


# ---------------------------------------------------------------------------
# Heuristic analysis
# ---------------------------------------------------------------------------

def test_analyze_clean_text_returns_authentic(engine: MisinformationEngine) -> None:
    result = engine.analyze("The central bank announced a routine rate adjustment today.")
    assert result == AnalysisResult(is_misinfo=0, confidence=0.95, hit_count=0)


def test_analyze_single_hit_is_low_confidence_flag(engine: MisinformationEngine) -> None:
    result = engine.analyze("This article mentions miracle cure once.")
    assert result == AnalysisResult(is_misinfo=1, confidence=0.40, hit_count=1)


def test_analyze_two_hits_is_moderate_flag(engine: MisinformationEngine) -> None:
    result = engine.analyze("miracle cure and a secret remedy in one sentence.")
    assert result == AnalysisResult(is_misinfo=1, confidence=0.65, hit_count=2)


def test_analyze_three_or_more_hits_is_high_flag(engine: MisinformationEngine) -> None:
    text = (
        "miracle cure secret remedy and doctors don't want you to know about "
        "the deep state behind it all."
    )
    result = engine.analyze(text)
    assert result.is_misinfo == 1
    assert result.confidence == 0.85
    assert result.hit_count >= 3


def test_analyze_is_case_insensitive(engine: MisinformationEngine) -> None:
    result = engine.analyze("MIRACLE CURE is what the article promises.")
    assert result.hit_count == 1


@pytest.mark.parametrize("text", ["", "   ", "\n\t  "])
def test_analyze_empty_text_raises(engine: MisinformationEngine, text: str) -> None:
    with pytest.raises(ValueError):
        engine.analyze(text)


# ---------------------------------------------------------------------------
# Fetcher injection
# ---------------------------------------------------------------------------

def test_extract_text_uses_injected_fetcher() -> None:
    captured: list[str] = []

    def fake_fetcher(url: str) -> tuple[str, str]:
        captured.append(url)
        return "Some Title", "some body text"

    eng = MisinformationEngine(fetcher=fake_fetcher)
    title, text = eng.extract_text("https://example.com/x")

    assert captured == ["https://example.com/x"]
    assert title == "Some Title"
    assert text == "some body text"


def test_extract_text_propagates_fetcher_errors() -> None:
    def boom(url: str) -> tuple[str, str]:
        raise RuntimeError("network down")

    eng = MisinformationEngine(fetcher=boom)
    with pytest.raises(RuntimeError, match="network down"):
        eng.extract_text("https://example.com")
