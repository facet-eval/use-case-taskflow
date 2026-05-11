from __future__ import annotations

import sqlite3

_INITIAL_SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    due_at TEXT,
    created_at TEXT NOT NULL,
    completed_at TEXT
)
"""


def apply_migrations(conn: sqlite3.Connection) -> None:
    conn.executescript(_INITIAL_SCHEMA)
