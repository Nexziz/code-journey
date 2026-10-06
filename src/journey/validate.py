"""Quality checks for task packs: does the reference solution pass, does the starter not?"""

from __future__ import annotations

import re
import shutil
import tempfile
import time
from collections.abc import Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import runners
from .tasks import Catalog, Task


def validate_task(task: Task, catalog: Catalog) -> list[str]:
    problems: list[str] = []

    for rule in (*task.require, *task.forbid):
        try:
            re.compile(rule.pattern)
        except re.error as exc:
            problems.append(f"bad regex {rule.pattern!r}: {exc}")
    if task.harness_path and not task.harness_path.is_file():
        problems.append(f"harness {task.harness} does not exist")
    if not 100 <= task.rating <= 3000:
        problems.append(f"rating {task.rating} looks wrong")
    if task.par_minutes < 1:
        problems.append("par_minutes must be at least 1")
    if catalog.level(task.language, task.level) is None:
        problems.append(f"level {task.level} is not listed in {task.language}/levels.toml")
    takes_input = any(c.args or c.stdin for c in task.cases)
    if takes_input and not any(c.hidden for c in task.cases) and task.rated:
        problems.append("daily and weekly tasks should have at least one hidden case")

    if not task.solution_dir.is_dir():
        return problems + ["no solution/ directory"]
    missing = [f for f in task.files if not (task.solution_dir / f).is_file()]
    if missing:
        return problems + [f"solution/ is missing {', '.join(missing)}"]

    result = runners.grade(task, task.solution_dir, include_hidden=True)
    if not result.passed:
        failed = [
            f"{c.name}: {c.detail.splitlines()[0] if c.detail else ''}"
            for c in result.checks
            if not c.ok
        ]
        problems.append("the reference solution fails: " + "; ".join(failed))
    if result.style:
        problems.append(f"the reference solution has style notes: {result.style[0]}")

    # Mutants are deliberately wrong solutions: the tests must reject every one of them.
    mutants = task.root / "mutants"
    if mutants.is_dir():
        for mutant in sorted(p for p in mutants.iterdir() if p.is_dir()):
            if runners.grade(task, mutant, include_hidden=True).passed:
                problems.append(f"mutant '{mutant.name}' passes: the tests do not catch it")

    if task.starter_dir.is_dir():
        with tempfile.TemporaryDirectory(prefix="journey-starter-") as tmp:
            shutil.copytree(task.starter_dir, tmp, dirs_exist_ok=True)
            starter = runners.grade(task, Path(tmp), include_hidden=True)
        if starter.passed:
            problems.append("the starter files already pass; the learner would have nothing to do")
    return problems


def iter_validate(
    tasks: Iterable[Task], catalog: Catalog, *, workers: int = 4
) -> Iterator[tuple[Task, list[str], float]]:
    """Validate tasks a few at a time, yielding (task, problems, seconds) in the given order."""

    def one(task: Task) -> tuple[Task, list[str], float]:
        started = time.time()
        return task, validate_task(task, catalog), time.time() - started

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        yield from pool.map(one, list(tasks))
