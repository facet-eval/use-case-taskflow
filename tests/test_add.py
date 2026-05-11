from __future__ import annotations

import sqlite3
from pathlib import Path

from click.testing import CliRunner

from taskflow.cli import main


def test_add_creates_task(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(main, ["add", "buy milk"])
    assert result.exit_code == 0, result.output
    assert "Created task 1: buy milk" in result.output

    with sqlite3.connect(tmp_db_path) as conn:
        rows = conn.execute("SELECT title, status FROM tasks").fetchall()
    assert rows == [("buy milk", "pending")]


def test_add_persists_due_and_description(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(
        main,
        [
            "add",
            "call mom",
            "--description",
            "weekly check-in",
            "--due",
            "2026-05-12T18:00:00+00:00",
        ],
    )
    assert result.exit_code == 0, result.output

    with sqlite3.connect(tmp_db_path) as conn:
        row = conn.execute("SELECT title, description, due_at FROM tasks").fetchone()
    assert row == ("call mom", "weekly check-in", "2026-05-12T18:00:00+00:00")


def test_add_rejects_empty_title(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(main, ["add", ""])
    assert result.exit_code != 0
    assert "Title must not be empty" in result.output


def test_add_rejects_invalid_due(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(main, ["add", "task", "--due", "not a date"])
    assert result.exit_code != 0
    assert "Could not parse date" in result.output
