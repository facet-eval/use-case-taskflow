from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from click.testing import CliRunner


@pytest.fixture()
def tmp_db_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    db = tmp_path / "tasks.db"
    monkeypatch.setenv("TASKFLOW_DB", str(db))
    return db


@pytest.fixture()
def runner() -> Iterator[CliRunner]:
    yield CliRunner()
