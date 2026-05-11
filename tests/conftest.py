from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from click.testing import CliRunner

from taskflow.db.connection import connect
from taskflow.db.schema import apply_migrations
from taskflow.repository import TaskRepository


@pytest.fixture()
def tmp_db_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    db = tmp_path / "tasks.db"
    monkeypatch.setenv("TASKFLOW_DB", str(db))
    return db


@pytest.fixture()
def runner() -> Iterator[CliRunner]:
    yield CliRunner()


@pytest.fixture()
def repo(tmp_db_path: Path) -> Iterator[TaskRepository]:
    with connect(tmp_db_path) as conn:
        apply_migrations(conn)
        yield TaskRepository(conn)
