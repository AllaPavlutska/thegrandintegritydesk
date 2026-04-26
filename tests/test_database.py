"""Tests for ``analyzer.database``."""

from __future__ import annotations

from pathlib import Path

import pytest

from analyzer.database import DatabaseManager


@pytest.fixture()
def db(tmp_path: Path) -> DatabaseManager:
    return DatabaseManager(db_name=str(tmp_path / "test.db"))


def test_initialize_creates_table(db: DatabaseManager) -> None:
    assert db.count_detections() == 0


def test_log_detection_persists_row(db: DatabaseManager) -> None:
    db.log_detection("https://example.com", "A title", 1, 0.85)
    assert db.count_detections() == 1


def test_log_detection_coerces_types(db: DatabaseManager) -> None:
    db.log_detection("https://example.com", "T", True, 1)  # ints/bools accepted
    assert db.count_detections() == 1


def test_multiple_log_calls_accumulate(db: DatabaseManager) -> None:
    for i in range(3):
        db.log_detection(f"https://example.com/{i}", "T", 0, 0.95)
    assert db.count_detections() == 3
