"""Tests for ``analyzer.validators``."""

from __future__ import annotations

import pytest

from analyzer.validators import is_local_url


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost",
        "http://localhost:8080/path",
        "http://127.0.0.1",
        "http://192.168.1.5/x",
        "http://10.0.0.1",
        "http://172.16.0.1",
        "http://172.31.255.255/x",
    ],
)
def test_is_local_url_true(url: str) -> None:
    assert is_local_url(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com",
        "https://nytimes.com/article",
        "http://203.0.113.5",  # public IP range
        "http://172.15.0.1",   # just outside private range
        "http://172.32.0.1",   # just outside private range
        "",
    ],
)
def test_is_local_url_false(url: str) -> None:
    assert is_local_url(url) is False
