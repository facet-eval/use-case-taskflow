from __future__ import annotations

import sqlite3

from taskflow.dates import format_iso, now_utc


def mark_done(conn: sqlite3.Connection, task_id: int) -> int:
    """Mark the task as done. Returns the number of rows updated (0 or 1)."""
    cursor = conn.execute(
        "UPDATE tasks SET status = 'done', completed_at = ? WHERE id = ?",
        (format_iso(now_utc()), task_id),
    )
    return cursor.rowcount


def delete(conn: sqlite3.Connection, task_id: int) -> int:
    """Delete the task. Returns the number of rows removed (0 or 1)."""
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return cursor.rowcount
