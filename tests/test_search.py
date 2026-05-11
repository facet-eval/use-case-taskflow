from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from taskflow.cli import main
from taskflow.repository import TaskRepository


def _seed(runner: CliRunner, specs: list[list[str]]) -> None:
    for args in specs:
        result = runner.invoke(main, ["add", *args])
        assert result.exit_code == 0, result.output


def test_search_single_term_match(tmp_db_path: Path, runner: CliRunner) -> None:
    _seed(runner, [["buy milk"], ["call mom"]])
    result = runner.invoke(main, ["search", "milk"])
    assert result.exit_code == 0, result.output
    assert "buy milk" in result.output
    assert "call mom" not in result.output


def test_search_multi_term_match(tmp_db_path: Path, runner: CliRunner) -> None:
    _seed(
        runner,
        [
            ["buy milk"],
            ["groceries: milk and bread"],
            ["call mom"],
        ],
    )
    result = runner.invoke(main, ["search", "milk bread"])
    assert result.exit_code == 0, result.output
    assert "groceries" in result.output
    assert "call mom" not in result.output


def test_search_ranking_prefers_more_matches(repo: TaskRepository) -> None:
    repo.add("milk")
    repo.add("milk milk milk")
    results = repo.search("milk")
    titles = [t.title for t in results]
    assert titles == ["milk milk milk", "milk"], (
        f"BM25 should rank denser matches higher; got {titles!r}"
    )


def test_search_no_match_returns_empty_message(tmp_db_path: Path, runner: CliRunner) -> None:
    _seed(runner, [["buy milk"]])
    result = runner.invoke(main, ["search", "xyzzy"])
    assert result.exit_code == 0, result.output
    assert "No tasks." in result.output

    json_result = runner.invoke(main, ["search", "xyzzy", "--json"])
    assert json_result.exit_code == 0, json_result.output
    assert json.loads(json_result.output) == []
