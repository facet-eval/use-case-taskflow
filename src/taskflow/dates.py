from __future__ import annotations

from datetime import UTC, datetime

from taskflow.errors import InvalidDate


def parse_due(value: str | None) -> datetime | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        if " " in text and "T" not in text:
            text = text.replace(" ", "T", 1)
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise InvalidDate(f"Could not parse date: {value!r}") from exc
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def format_iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat()


def now_utc() -> datetime:
    return datetime.now(tz=UTC)
