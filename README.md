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
taskflow search "milk"
```

The first command creates a task at `medium` priority (the default). The second creates one at `high`. The third filters the list view down to only the high-priority tasks.

The database file is created on first use. Override its location with:

```bash
export TASKFLOW_DB="$HOME/tasks.db"
```

## Priority

Every task has a `priority` of `low`, `medium`, or `high`. `medium` is the default — use `--priority high` to bump something up or `--priority low` to defer.

`taskflow list --priority <value>` filters; combine with `--status` and `--due-before` for AND-style narrowing. Priority is included in `taskflow list` output (the `PRIORITY` column) and in `taskflow export` for both JSON and CSV.

## Search

`taskflow search "<query>"` runs a full-text search over every task's title and description, using SQLite FTS5 with BM25 ranking — best matches first.

```bash
taskflow search "buy milk"
taskflow search "groceries" --limit 10
taskflow search "deadline" --json
```

Multi-term queries are AND-style by default (a task must contain both "buy" and "milk" to match `"buy milk"`). Empty queries are rejected with a friendly error. The first time you run it after upgrading, existing tasks are indexed automatically — no manual reindex needed.

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
