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
```

Prints something like `Created task 1: buy milk`.

The database file is created on first use. Override its location with:

```bash
export TASKFLOW_DB="$HOME/tasks.db"
```

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
