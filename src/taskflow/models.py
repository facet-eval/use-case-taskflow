from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    description: str
    status: str
    due_at: datetime | None
    created_at: datetime
    completed_at: datetime | None
    priority: str
