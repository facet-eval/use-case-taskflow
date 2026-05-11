# taskflow

A small Python CLI for managing personal tasks, backed by SQLite.

No network. No accounts. No plugins. Your tasks live in a single SQLite file under `$XDG_DATA_HOME/taskflow/tasks.db` (or wherever `TASKFLOW_DB` points).

## Install

```bash
pip install -e .
```

Requires Python 3.11 or newer.

## Quickstart

```bash
taskflow add "buy milk" --due "2026-05-12 18:00"
taskflow add "fix prod" --priority high
taskflow list --priority high
```

The first command creates a task at `medium` priority (the default). The second creates one at `high`. The third filters the list view down to only the high-priority tasks.

The database file is created on first use. Override its location with:

```bash
export TASKFLOW_DB="$HOME/tasks.db"
```

## Priority

Every task has a `priority` of `low`, `medium`, or `high`. `medium` is the default — use `--priority high` to bump something up or `--priority low` to defer.

`taskflow list --priority <value>` filters; combine with `--status` and `--due-before` for AND-style narrowing. Priority is included in `taskflow list` output (the `PRIORITY` column) and in `taskflow export` for both JSON and CSV.

## Development

```bash
pip install -e ".[dev]"
pytest -q
ruff check .
ruff format --check .
mypy --strict src/
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for branching, commits, and review conventions.

## License

MIT — see [`LICENSE`](LICENSE).
