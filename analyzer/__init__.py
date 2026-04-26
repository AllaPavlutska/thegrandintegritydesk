"""The Grand Integrity Desk — misinformation URL analyzer.

A small package that splits the previously-monolithic ``app.py`` into
focused, independently-testable modules.
"""

from analyzer.database import DatabaseManager
from analyzer.engine import DomainStatus, MisinformationEngine
from analyzer.validators import is_local_url

__all__ = [
    "DatabaseManager",
    "DomainStatus",
    "MisinformationEngine",
    "is_local_url",
]
