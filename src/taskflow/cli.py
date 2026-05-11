from __future__ import annotations

import click

from taskflow import __version__


@click.group()
@click.version_option(__version__, prog_name="taskflow")
def main() -> None:
    """Manage personal tasks from the command line."""


from taskflow import commands  # noqa: F401, E402
