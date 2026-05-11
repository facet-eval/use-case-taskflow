from __future__ import annotations

import sys
from pathlib import Path

import click

from taskflow import __version__
from taskflow.db.connection import connect, default_db_path
from taskflow.db.schema import apply_migrations
from taskflow.export import write_csv, write_json
from taskflow.listing import ListFilters
from taskflow.repository import TaskRepository


@click.group()
@click.version_option(__version__, prog_name="taskflow")
def main() -> None:
    """Manage personal tasks from the command line."""


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


from taskflow import commands  # noqa: F401, E402
