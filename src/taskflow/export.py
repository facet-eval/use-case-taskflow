from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from typing import TextIO

from taskflow.dates import format_iso
from taskflow.models import Task

_FIELDS = (
    "id",
    "title",
    "description",
    "status",
    "due_at",
    "created_at",
    "completed_at",
)


def _task_to_dict(task: Task) -> dict[str, object]:
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "due_at": format_iso(task.due_at) if task.due_at else None,
        "created_at": format_iso(task.created_at),
        "completed_at": format_iso(task.completed_at) if task.completed_at else None,
    }


def write_json(tasks: Iterable[Task], fp: TextIO) -> None:
    payload = [_task_to_dict(task) for task in tasks]
    json.dump(payload, fp, indent=2)
    fp.write("\n")


def write_csv(tasks: Iterable[Task], fp: TextIO) -> None:
    writer = csv.DictWriter(fp, fieldnames=_FIELDS)
    writer.writeheader()
    for task in tasks:
        row = _task_to_dict(task)
        writer.writerow({key: ("" if row[key] is None else row[key]) for key in _FIELDS})
