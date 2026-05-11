from __future__ import annotations


class TaskflowError(Exception):
    """Base class for all taskflow errors."""


class InvalidDate(TaskflowError):
    """Raised when a date string cannot be parsed."""
