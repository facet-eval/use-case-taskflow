from __future__ import annotations

import os
import shutil
import sqlite3
import subprocess
from pathlib import Path

import pytest

_TASKFLOW_BIN = shutil.which("taskflow")
_SRC_DIR = Path(__file__).resolve().parent.parent / "src"


@pytest.mark.skipif(_TASKFLOW_BIN is None, reason="taskflow CLI not installed")
def test_concurrent_adds_persist_all_writes(tmp_path: Path) -> None:
    """Regression: parallel `taskflow add` invocations must not lose writes or fail
    with 'database is locked'.

    The architectural patology (deferred BEGIN + journal_mode=delete) lets two
    writers each take a SHARED lock and then race for the upgrade to RESERVED;
    one of them gets `OperationalError: database is locked` after `busy_timeout`.
    The fix (PRAGMA journal_mode=WAL + isolation_level='IMMEDIATE') makes the
    writer take the lock at BEGIN time, so concurrent writers serialize cleanly
    instead of racing for an upgrade.

    Note on test reliability: on modern hardware with the default 5s
    `busy_timeout`, contention is usually absorbed and this test passes pre-fix
    too. It still serves as a forward-guard: if the fix is reverted and run on
    slower I/O, a busier scheduler, or with a shorter `busy_timeout`, both
    assertions (no failed exits, exact row count) catch the regression.

    PYTHONPATH is set in the subprocess env to bypass the macOS iCloud `.pth`
    UF_HIDDEN flag (see CLAUDE.md § 5). On Linux CI the override is harmless.
    """
    db = tmp_path / "concurrent.db"
    n = 20
    env = {
        **os.environ,
        "TASKFLOW_DB": str(db),
        "PYTHONPATH": str(_SRC_DIR),
    }
    procs = [
        subprocess.Popen(
            [str(_TASKFLOW_BIN), "add", f"task {i}"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        for i in range(n)
    ]

    failures: list[str] = []
    for proc in procs:
        proc.wait(timeout=30)
        if proc.returncode != 0:
            stderr = proc.stderr.read().decode() if proc.stderr else "(no stderr)"
            failures.append(f"exit {proc.returncode}: {stderr.strip()}")

    assert not failures, f"{len(failures)}/{n} writers failed:\n" + "\n".join(failures)

    with sqlite3.connect(db) as conn:
        count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    assert count == n, f"expected {n} rows after concurrent adds, got {count}"
