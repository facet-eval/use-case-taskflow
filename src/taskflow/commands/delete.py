from __future__ import annotations

import click

from taskflow.cli import main
from taskflow.db.connection import connect_for_write, default_db_path
from taskflow.db.schema import apply_migrations
from taskflow.repository import TaskRepository


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
