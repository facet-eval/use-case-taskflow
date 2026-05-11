from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from taskflow.dates import format_iso, parse_due

_BASE_COLUMNS = "id, title, description, status, due_at, created_at, completed_at, priority"


@dataclass(frozen=True, slots=True)
class ListFilters:
    status: str | None = None
    due_before: datetime | None = None

    @classmethod
    def from_options(cls, status: str | None, due_before: str | None) -> ListFilters:
        return cls(status=status, due_before=parse_due(due_before))


def build_query(filters: ListFilters) -> tuple[str, tuple[Any, ...]]:
    where_clauses: list[str] = []
    params: list[Any] = []
    if filters.status:
        where_clauses.append("status = ?")
        params.append(filters.status)
    if filters.due_before is not None:
        where_clauses.append("due_at IS NOT NULL AND due_at < ?")
        params.append(format_iso(filters.due_before))
    where_sql = ""
    if where_clauses:
        where_sql = " WHERE " + " AND ".join(where_clauses)
    sql = f"SELECT {_BASE_COLUMNS} FROM tasks{where_sql} ORDER BY id"
    return sql, tuple(params)
