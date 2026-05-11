from __future__ import annotations

import sqlite3
from datetime import datetime

from taskflow.dates import format_iso, now_utc
from taskflow.listing import ListFilters, build_query
from taskflow.models import Task

_BASE_COLUMNS = "id, title, description, status, due_at, created_at, completed_at, priority"


class TaskRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def add(
        self,
        title: str,
        description: str = "",
        due_at: datetime | None = None,
        priority: str = "medium",
    ) -> int:
        created_at = now_utc()
        cursor = self._conn.execute(
            "INSERT INTO tasks (title, description, due_at, created_at, priority) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                title,
                description,
                format_iso(due_at) if due_at else None,
                format_iso(created_at),
                priority,
            ),
        )
        return int(cursor.lastrowid or 0)

    def list_tasks(self, filters: ListFilters) -> list[Task]:
        sql, params = build_query(filters)
        rows = self._conn.execute(sql, params).fetchall()
        return [_row_to_task(row) for row in rows]

    def get(self, task_id: int) -> Task | None:
        sql = f"SELECT {_BASE_COLUMNS} FROM tasks WHERE id = ?"
        row = self._conn.execute(sql, (task_id,)).fetchone()
        return _row_to_task(row) if row else None

    def mark_done(self, task_id: int) -> int:
        cursor = self._conn.execute(
            "UPDATE tasks SET status = 'done', completed_at = ? WHERE id = ?",
            (format_iso(now_utc()), task_id),
        )
        return cursor.rowcount

    def delete(self, task_id: int) -> int:
        cursor = self._conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cursor.rowcount


def _row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        status=row["status"],
        due_at=datetime.fromisoformat(row["due_at"]) if row["due_at"] else None,
        created_at=datetime.fromisoformat(row["created_at"]),
        completed_at=(datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None),
        priority=row["priority"],
    )
