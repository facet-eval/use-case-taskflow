from __future__ import annotations

import click

from taskflow.cli import main
from taskflow.db.connection import connect, default_db_path
from taskflow.db.schema import apply_migrations
from taskflow.errors import TaskflowError
from taskflow.listing import ListFilters
from taskflow.output import render_json, render_table
from taskflow.repository import TaskRepository


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
