from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from taskflow.cli import main


def _seed(runner: CliRunner, specs: list[list[str]]) -> None:
    for args in specs:
        result = runner.invoke(main, ["add", *args])
        assert result.exit_code == 0, result.output


def test_list_empty_db_says_no_tasks(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(main, ["list"])
    assert result.exit_code == 0, result.output
    assert "No tasks." in result.output


def test_list_rejects_unknown_status_value(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(main, ["list", "--status", "archived"])
    assert result.exit_code != 0


def test_list_due_before_invalid_value_fails(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(main, ["list", "--due-before", "garbage"])
    assert result.exit_code != 0
    assert "Could not parse date" in result.output


def test_list_json_returns_valid_array(tmp_db_path: Path, runner: CliRunner) -> None:
    _seed(
        runner,
        [
            [
                "buy milk",
                "--description",
                "from the store",
                "--due",
                "2026-05-12T18:00:00+00:00",
            ]
        ],
    )
    result = runner.invoke(main, ["list", "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert isinstance(payload, list)
    assert len(payload) == 1
    item = payload[0]
    assert item["title"] == "buy milk"
    assert item["description"] == "from the store"
    assert item["status"] == "pending"
    assert item["due_at"] == "2026-05-12T18:00:00+00:00"
    assert item["completed_at"] is None
    assert "created_at" in item


def test_list_json_empty_db_returns_empty_array(tmp_db_path: Path, runner: CliRunner) -> None:
    result = runner.invoke(main, ["list", "--json"])
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == []
