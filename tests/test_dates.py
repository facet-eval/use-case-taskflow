from __future__ import annotations

import time
from collections.abc import Iterator
from datetime import UTC, datetime

import pytest

from taskflow.dates import format_iso, parse_due
from taskflow.errors import InvalidDate


def test_parse_due_returns_none_for_none() -> None:
    assert parse_due(None) is None


def test_parse_due_returns_none_for_empty_string() -> None:
    assert parse_due("") is None
    assert parse_due("   ") is None


def test_parse_due_round_trips_explicit_utc() -> None:
    parsed = parse_due("2026-05-12T18:00:00+00:00")
    assert parsed == datetime(2026, 5, 12, 18, 0, tzinfo=UTC)
    assert format_iso(parsed) == "2026-05-12T18:00:00+00:00"


def test_parse_due_accepts_space_separator() -> None:
    parsed = parse_due("2026-05-12 18:00")
    assert parsed is not None
    assert parsed.tzinfo is not None


def test_parse_due_raises_on_invalid_input() -> None:
    with pytest.raises(InvalidDate):
        parse_due("not a date")


def test_format_iso_normalizes_to_utc() -> None:
    naive = datetime(2026, 5, 12, 18, 0, tzinfo=UTC)
    assert format_iso(naive).endswith("+00:00")


@pytest.fixture
def tz_bogota(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Pin the process timezone to America/Bogota (UTC-5) for the duration of the test.

    `time.tzset()` is required because Python reads the TZ env var via libc, and
    setenv alone doesn't refresh libc's cached value. The teardown re-runs tzset
    so subsequent tests don't see the pinned zone.
    """
    monkeypatch.setenv("TZ", "America/Bogota")
    time.tzset()
    yield
    time.tzset()


def test_parse_due_naive_input_interpreted_as_local_not_utc(tz_bogota: None) -> None:
    """Regression: naive datetimes were stamped as UTC instead of converted from local time.

    Under TZ=America/Bogota (UTC-5), the input `2026-05-12 18:00` is local 18:00,
    which is UTC 23:00 the same day. Before the fix, `parse_due` returned
    `2026-05-12T18:00:00+00:00` — wrong by 5 hours.
    """
    result = parse_due("2026-05-12 18:00")
    assert result == datetime(2026, 5, 12, 23, 0, tzinfo=UTC)
