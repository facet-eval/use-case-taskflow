from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from taskflow.cli import main


def test_add_rejects_empty_title(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(main, ["add", ""])
    assert result.exit_code != 0
    assert "Title must not be empty" in result.output


def test_add_rejects_invalid_due(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(main, ["add", "task", "--due", "not a date"])
    assert result.exit_code != 0
    assert "Could not parse date" in result.output
