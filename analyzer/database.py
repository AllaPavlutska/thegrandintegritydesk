"""SQLite persistence for inspection results."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator

_SCHEMA = """
CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    article_title TEXT,
    is_misinfo INTEGER,
    confidence_score REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""


class DatabaseManager:
    """Thin SQLite wrapper for logging detection results."""

    def __init__(self, db_name: str = "safety_pipeline.db") -> None:
        self.db_name = db_name
        self._initialize_db()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _initialize_db(self) -> None:
        with self._connect() as conn:
            conn.execute(_SCHEMA)

    def log_detection(
        self,
        url: str,
        title: str,
        is_misinfo: int,
        confidence: float,
    ) -> None:
        """Persist a single detection record."""
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO detections (url, article_title, is_misinfo, confidence_score)
                VALUES (?, ?, ?, ?)
                """,
                (url, title, int(is_misinfo), float(confidence)),
            )

    def count_detections(self) -> int:
        """Return the total number of logged detections (used by tests)."""
        with self._connect() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM detections")
            row = cursor.fetchone()
            return int(row[0]) if row else 0
