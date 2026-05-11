from __future__ import annotations

from datetime import UTC, datetime

from taskflow.listing import ListFilters
from taskflow.repository import TaskRepository


def test_repository_add_inserts_row(repo: TaskRepository) -> None:
    task_id = repo.add("buy milk")
    assert task_id == 1
    task = repo.get(task_id)
    assert task is not None
    assert task.title == "buy milk"
    assert task.status == "pending"


def test_repository_add_persists_optional_fields(repo: TaskRepository) -> None:
    task_id = repo.add(
        "call mom",
        description="weekly check-in",
        due_at=datetime(2026, 5, 12, 18, 0, tzinfo=UTC),
    )
    task = repo.get(task_id)
    assert task is not None
    assert task.description == "weekly check-in"
    assert task.due_at == datetime(2026, 5, 12, 18, 0, tzinfo=UTC)


def test_repository_list_returns_all_tasks(repo: TaskRepository) -> None:
    repo.add("a")
    repo.add("b")
    tasks = repo.list_tasks(ListFilters())
    assert [t.title for t in tasks] == ["a", "b"]


def test_repository_list_filter_by_status(repo: TaskRepository) -> None:
    repo.add("a")
    repo.add("b")
    repo.mark_done(1)
    pending = repo.list_tasks(ListFilters(status="pending"))
    done = repo.list_tasks(ListFilters(status="done"))
    assert [t.title for t in pending] == ["b"]
    assert [t.title for t in done] == ["a"]


def test_repository_list_filter_status_done_returns_empty(repo: TaskRepository) -> None:
    repo.add("only pending")
    done = repo.list_tasks(ListFilters(status="done"))
    assert done == []


def test_repository_list_filter_by_due_before(repo: TaskRepository) -> None:
    repo.add("early", due_at=datetime(2026, 1, 1, tzinfo=UTC))
    repo.add("late", due_at=datetime(2026, 12, 31, tzinfo=UTC))
    repo.add("no_due")
    cutoff = datetime(2026, 6, 1, tzinfo=UTC)
    tasks = repo.list_tasks(ListFilters(due_before=cutoff))
    assert [t.title for t in tasks] == ["early"]
