from __future__ import annotations

import click

from taskflow import __version__
from taskflow.dates import format_iso, now_utc, parse_due
from taskflow.db.connection import connect, default_db_path
from taskflow.db.schema import apply_migrations
from taskflow.errors import TaskflowError


@click.group()
@click.version_option(__version__, prog_name="taskflow")
def main() -> None:
    """Manage personal tasks from the command line."""


@main.command("add")
@click.argument("title")
@click.option("--description", default="", help="Optional task description.")
@click.option(
    "--due",
    default=None,
    help="Optional due date (ISO 8601 or 'YYYY-MM-DD HH:MM').",
)
def add_command(title: str, description: str, due: str | None) -> None:
    """Create a new task."""
    if not title.strip():
        raise click.UsageError("Title must not be empty.")
    try:
        due_at = parse_due(due)
    except TaskflowError as exc:
        raise click.ClickException(str(exc)) from exc

    created_at = now_utc()
    with connect(default_db_path()) as conn:
        apply_migrations(conn)
        cursor = conn.execute(
            "INSERT INTO tasks (title, description, due_at, created_at) VALUES (?, ?, ?, ?)",
            (
                title.strip(),
                description,
                format_iso(due_at) if due_at else None,
                format_iso(created_at),
            ),
        )
        task_id = cursor.lastrowid

    click.echo(f"Created task {task_id}: {title.strip()}")
