"""CLI subcommand registrations.

Importing this package triggers each submodule's ``@main.command`` decorator,
which attaches the subcommand to the root ``click.group`` defined in
``taskflow.cli``. The root entrypoint imports this package once for its
side-effects.
"""

from taskflow.commands import add  # noqa: F401
