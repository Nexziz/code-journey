"""Turning a grade into progress: attempts, stars, rating changes and level-ups."""

from __future__ import annotations

from dataclasses import dataclass

from .curriculum import completed_levels
from .runners import GradeResult
from .scoring import Performance, performance, rating_update
from .store import Store
from .tasks import Catalog, Level, Task


@dataclass
class Outcome:
    task: Task
    passed: bool
    result: GradeResult
    attempt_no: int
    failed_attempts: int
    active_seconds: float
    performance: Performance | None = None
    repeat: bool = False
    rating_before: float | None = None
    rating_after: float | None = None
    expected: float | None = None
    level_up: Level | None = None


def _apply_rating(store: Store, task: Task, score: float) -> tuple[float, float, float]:
    rating, games = store.rating(task.language)
    new, expected, _ = rating_update(rating, games, task.rating, score, task.kind)
    store.set_rating(task.language, new, games + 1)
    return rating, new, expected


def submit(
    store: Store,
    catalog: Catalog,
    task: Task,
    result: GradeResult,
    *,
    commit: str | None,
    now: float,
) -> Outcome:
    """Record one graded push for the task you are working on."""
    if store.state(task.id) is None:
        raise LookupError(f"{task.id} is not in progress")
    active = store.elapsed(task.id, now)
    store.bump_attempt(task.id, failed=not result.passed)
    state = store.state(task.id)
    store.add_attempt(task.id, now, commit, result.passed, active, result.summary())
    outcome = Outcome(
        task, result.passed, result, state["attempts"], state["failed_attempts"], active
    )
    if not result.passed:
        return outcome

    perf = performance(
        rated=task.rated,
        failed_attempts=state["failed_attempts"],
        active_seconds=active,
        par_minutes=task.par_minutes,
        style_issues=len(result.style),
    )
    repeat = bool(state["repeat"])
    levels_before = completed_levels(store, catalog, task.language)
    before = after = expected = None
    if task.rated and not repeat:
        before, after, expected = _apply_rating(store, task, perf.score)
    store.add_completion(
        task_id=task.id,
        language=task.language,
        kind=task.kind,
        ts=now,
        gave_up=0,
        repeat=int(repeat),
        score=perf.score,
        stars=perf.stars,
        active_seconds=active,
        failed_attempts=state["failed_attempts"],
        rating_before=before,
        rating_after=after,
        expected=expected,
    )
    store.drop_state(task.id)
    if store.get_meta("current") == task.id:
        store.clear_meta("current")

    outcome.performance = perf
    outcome.repeat = repeat
    outcome.rating_before, outcome.rating_after, outcome.expected = before, after, expected
    levels_after = completed_levels(store, catalog, task.language)
    if levels_after > levels_before:
        outcome.level_up = catalog.level(task.language, levels_after)
    return outcome


def give_up(store: Store, task: Task, now: float) -> tuple[float, float] | None:
    """Abandon a task. Rated tasks count as a loss (score 0); learning tasks cost nothing.

    Returns (rating before, rating after) when the rating changed.
    """
    state = store.state(task.id)
    if state is None:
        raise LookupError(f"{task.id} is not in progress")
    active = store.elapsed(task.id, now)
    change = None
    if task.rated and not state["repeat"]:
        before, after, expected = _apply_rating(store, task, 0.0)
        store.add_completion(
            task_id=task.id,
            language=task.language,
            kind=task.kind,
            ts=now,
            gave_up=1,
            repeat=0,
            score=0.0,
            stars=0,
            active_seconds=active,
            failed_attempts=state["failed_attempts"],
            rating_before=before,
            rating_after=after,
            expected=expected,
        )
        change = (before, after)
    store.drop_state(task.id)
    if store.get_meta("current") == task.id:
        store.clear_meta("current")
    return change
