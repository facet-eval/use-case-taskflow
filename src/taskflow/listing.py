from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any

from taskflow.dates import format_iso
from taskflow.models import Task

_BASE_COLUMNS = "id, title, description, status, due_at, created_at, completed_at"


def build_query(filters: dict[str, Any]) -> tuple[str, tuple[Any, ...]]:
    where_clauses: list[str] = []
    params: list[Any] = []
    if filters.get("status"):
        where_clauses.append("status = ?")
        params.append(filters["status"])
    if filters.get("due_before") is not None:
        where_clauses.append("due_at IS NOT NULL AND due_at < ?")
        params.append(format_iso(filters["due_before"]))
    where_sql = ""
    if where_clauses:
        where_sql = " WHERE " + " AND ".join(where_clauses)
    sql = f"SELECT {_BASE_COLUMNS} FROM tasks{where_sql} ORDER BY id"
    return sql, tuple(params)


def fetch_tasks(conn: sqlite3.Connection, filters: dict[str, Any]) -> list[Task]:
    sql, params = build_query(filters)
    rows = conn.execute(sql, params).fetchall()
    return [_row_to_task(row) for row in rows]


def _row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        status=row["status"],
        due_at=datetime.fromisoformat(row["due_at"]) if row["due_at"] else None,
        created_at=datetime.fromisoformat(row["created_at"]),
        completed_at=(
            datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None
        ),
    )
