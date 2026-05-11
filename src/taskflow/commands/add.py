from __future__ import annotations

import click

from taskflow.cli import main
from taskflow.dates import parse_due
from taskflow.db.connection import connect_for_write, default_db_path
from taskflow.db.schema import apply_migrations
from taskflow.errors import TaskflowError
from taskflow.repository import TaskRepository


@main.command("add")
@click.argument("title")
@click.option("--description", default="", help="Optional task description.")
@click.option(
    "--due",
    default=None,
    help="Optional due date (ISO 8601 or 'YYYY-MM-DD HH:MM').",
)
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"]),
    default="medium",
    help="Task priority. Defaults to medium.",
)
def add_command(title: str, description: str, due: str | None, priority: str) -> None:
    """Create a new task."""
    if not title.strip():
        raise click.UsageError("Title must not be empty.")
    try:
        due_at = parse_due(due)
    except TaskflowError as exc:
        raise click.ClickException(str(exc)) from exc

    with connect_for_write(default_db_path()) as conn:
        apply_migrations(conn)
        repo = TaskRepository(conn)
        task_id = repo.add(title.strip(), description, due_at, priority)

    click.echo(f"Created task {task_id}: {title.strip()}")
