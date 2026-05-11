from __future__ import annotations

import click

from taskflow.cli import main
from taskflow.db.connection import connect_for_write, default_db_path
from taskflow.db.schema import apply_migrations
from taskflow.repository import TaskRepository


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
