from __future__ import annotations

import click

from taskflow.cli import main
from taskflow.db.connection import connect, default_db_path
from taskflow.db.schema import apply_migrations
from taskflow.output import render_json, render_table
from taskflow.repository import TaskRepository


@main.command("search")
@click.argument("query")
@click.option(
    "--limit",
    type=int,
    default=50,
    help="Maximum number of results to return.",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    default=False,
    help="Emit a JSON array instead of a table.",
)
def search_command(query: str, limit: int, as_json: bool) -> None:
    """Full-text search over task title and description."""
    with connect(default_db_path()) as conn:
        apply_migrations(conn)
        repo = TaskRepository(conn)
        tasks = repo.search(query, limit)
    if as_json:
        click.echo(render_json(tasks))
    else:
        click.echo(render_table(tasks))
