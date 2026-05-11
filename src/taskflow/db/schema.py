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
    _add_priority_column_if_missing(conn)


def _add_priority_column_if_missing(conn: sqlite3.Connection) -> None:
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(tasks)")}
    if "priority" in columns:
        return
    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN priority TEXT NOT NULL DEFAULT 'medium'")
    except sqlite3.OperationalError as exc:
        if "duplicate column" not in str(exc).lower():
            raise
