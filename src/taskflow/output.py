from __future__ import annotations

import json
from collections.abc import Iterable

from taskflow.dates import format_iso
from taskflow.models import Task


def render_table(tasks: Iterable[Task]) -> str:
    items = list(tasks)
    if not items:
        return "No tasks."
    headers = ("ID", "STATUS", "DUE", "TITLE")
    rows = [
        (
            str(task.id),
            task.status,
            format_iso(task.due_at) if task.due_at else "-",
            task.title,
        )
        for task in items
    ]
    widths = [max(len(row[i]) for row in [headers, *rows]) for i in range(len(headers))]
    sep = "  "
    lines = [sep.join(headers[i].ljust(widths[i]) for i in range(len(headers)))]
    lines.append(sep.join("-" * widths[i] for i in range(len(headers))))
    for row in rows:
        lines.append(sep.join(row[i].ljust(widths[i]) for i in range(len(headers))))
    return "\n".join(lines)


def render_json(tasks: Iterable[Task]) -> str:
    payload = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_at": format_iso(task.due_at) if task.due_at else None,
            "created_at": format_iso(task.created_at),
            "completed_at": (
                format_iso(task.completed_at) if task.completed_at else None
            ),
        }
        for task in tasks
    ]
    return json.dumps(payload, indent=2)
