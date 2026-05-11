from __future__ import annotations


class TaskflowError(Exception):
    """Base class for all taskflow errors."""


class InvalidDate(TaskflowError):
    """Raised when a date string cannot be parsed."""


class InvalidQuery(TaskflowError):
    """Raised when a search query is empty or otherwise invalid."""
