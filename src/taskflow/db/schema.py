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

_FTS_TABLE = """
CREATE VIRTUAL TABLE IF NOT EXISTS tasks_fts USING fts5(
    title,
    description,
    content='tasks',
    content_rowid='id'
)
"""


def apply_migrations(conn: sqlite3.Connection) -> None:
    conn.executescript(_INITIAL_SCHEMA)
    _add_priority_column_if_missing(conn)
    _create_fts_table_if_missing(conn)


def _add_priority_column_if_missing(conn: sqlite3.Connection) -> None:
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(tasks)")}
    if "priority" in columns:
        return
    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN priority TEXT NOT NULL DEFAULT 'medium'")
    except sqlite3.OperationalError as exc:
        if "duplicate column" not in str(exc).lower():
            raise


def _create_fts_table_if_missing(conn: sqlite3.Connection) -> None:
    conn.executescript(_FTS_TABLE)
    conn.execute(
        "INSERT INTO tasks_fts(rowid, title, description) "
        "SELECT id, title, description FROM tasks "
        "WHERE id NOT IN (SELECT rowid FROM tasks_fts)"
    )
