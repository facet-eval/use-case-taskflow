from __future__ import annotations

import click

from taskflow import __version__
from taskflow.dates import format_iso, now_utc, parse_due
from taskflow.db.connection import connect, default_db_path
from taskflow.db.operations import delete as delete_task
from taskflow.db.operations import mark_done
from taskflow.db.schema import apply_migrations
from taskflow.errors import TaskflowError
from taskflow.listing import ListFilters, fetch_tasks
from taskflow.output import render_json, render_table


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
    "--json",
    "as_json",
    is_flag=True,
    default=False,
    help="Emit a JSON array instead of a table.",
)
def list_command(status: str | None, due_before: str | None, as_json: bool) -> None:
    """List tasks, optionally filtered by status and due date."""
    try:
        filters = ListFilters.from_options(status, due_before)
    except TaskflowError as exc:
        raise click.ClickException(str(exc)) from exc
    with connect(default_db_path()) as conn:
        apply_migrations(conn)
        tasks = fetch_tasks(conn, filters)
    if as_json:
        click.echo(render_json(tasks))
    else:
        click.echo(render_table(tasks))


@main.command("done")
@click.argument("task_id", type=int)
def done_command(task_id: int) -> None:
    """Mark a task as done."""
    with connect(default_db_path()) as conn:
        apply_migrations(conn)
        affected = mark_done(conn, task_id)
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
    with connect(default_db_path()) as conn:
        apply_migrations(conn)
        affected = delete_task(conn, task_id)
    if affected == 0:
        raise click.ClickException(f"No task with id {task_id}.")
    click.echo(f"Deleted task {task_id}.")
