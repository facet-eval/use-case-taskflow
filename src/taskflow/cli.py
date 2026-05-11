from __future__ import annotations

import sys
from pathlib import Path

import click

from taskflow import __version__
from taskflow.dates import parse_due
from taskflow.db.connection import connect, connect_for_write, default_db_path
from taskflow.db.schema import apply_migrations
from taskflow.errors import TaskflowError
from taskflow.export import write_csv, write_json
from taskflow.listing import ListFilters
from taskflow.output import render_json, render_table
from taskflow.repository import TaskRepository


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


@main.command("list")
@click.option(
    "--status",
    type=click.Choice(["pending", "done"]),
    default=None,
    help="Filter by task status.",
)
@click.option(
    "--due-before",
    default=None,
    help="Show only tasks due strictly before this ISO datetime.",
)
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"]),
    default=None,
    help="Filter by task priority.",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    default=False,
    help="Emit a JSON array instead of a table.",
)
def list_command(
    status: str | None,
    due_before: str | None,
    priority: str | None,
    as_json: bool,
) -> None:
    """List tasks, optionally filtered by status, due date, and priority."""
    try:
        filters = ListFilters.from_options(status, due_before, priority)
    except TaskflowError as exc:
        raise click.ClickException(str(exc)) from exc
    with connect(default_db_path()) as conn:
        apply_migrations(conn)
        repo = TaskRepository(conn)
        tasks = repo.list_tasks(filters)
    if as_json:
        click.echo(render_json(tasks))
    else:
        click.echo(render_table(tasks))


@main.command("done")
@click.argument("task_id", type=int)
def done_command(task_id: int) -> None:
    """Mark a task as done."""
    with connect_for_write(default_db_path()) as conn:
        apply_migrations(conn)
        repo = TaskRepository(conn)
        affected = repo.mark_done(task_id)
    if affected == 0:
        raise click.ClickException(f"No task with id {task_id}.")
    click.echo(f"Marked task {task_id} as done.")


@main.command("delete")
@click.argument("task_id", type=int)
@click.option(
    "--yes",
    is_flag=True,
    default=False,
    help="Skip the confirmation prompt (useful for scripts).",
)
def delete_command(task_id: int, yes: bool) -> None:
    """Delete a task."""
    if not yes and not click.confirm(f"Delete task {task_id}?", default=False):
        click.echo("Aborted.")
        return
    with connect_for_write(default_db_path()) as conn:
        apply_migrations(conn)
        repo = TaskRepository(conn)
        affected = repo.delete(task_id)
    if affected == 0:
        raise click.ClickException(f"No task with id {task_id}.")
    click.echo(f"Deleted task {task_id}.")


@main.command("export")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["json", "csv"]),
    required=True,
    help="Output format.",
)
@click.option(
    "--output",
    "-o",
    default="-",
    help="Output file path, or '-' for stdout (default).",
)
def export_command(fmt: str, output: str) -> None:
    """Export all tasks to JSON or CSV. Writes to stdout by default."""
    with connect(default_db_path()) as conn:
        apply_migrations(conn)
        repo = TaskRepository(conn)
        tasks = repo.list_tasks(ListFilters())
    if output == "-":
        if fmt == "json":
            write_json(tasks, sys.stdout)
        else:
            write_csv(tasks, sys.stdout)
        return
    out_path = Path(output)
    with out_path.open("w", encoding="utf-8", newline="") as fp:
        if fmt == "json":
            write_json(tasks, fp)
        else:
            write_csv(tasks, fp)
    click.echo(f"Exported {out_path}")
