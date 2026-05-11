from __future__ import annotations

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
