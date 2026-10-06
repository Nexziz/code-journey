"""One runner per language. A runner turns a directory of learner files into a GradeResult."""

from __future__ import annotations

from pathlib import Path

from ..tasks import Task
from . import c, python
from .base import Check, GradeResult

__all__ = ["Check", "GradeResult", "grade"]


def grade(task: Task, workdir: Path, *, include_hidden: bool = True) -> GradeResult:
    runner = {"c": c, "python": python}[task.language]
    return runner.grade(task, workdir, include_hidden=include_hidden)
