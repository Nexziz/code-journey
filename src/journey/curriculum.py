"""Progress through the curriculum, streaks, and picking the daily and weekly task."""

from __future__ import annotations

import random
from datetime import date, timedelta

from .store import Store
from .tasks import Catalog, Task


def completed_levels(store: Store, catalog: Catalog, language: str) -> int:
    """How many levels, counted from level 1 without gaps, have every task passed."""
    passed = store.passed_ids()
    done = 0
    for level in catalog.levels.get(language, []):
        tasks = catalog.curriculum(language, level.number)
        if tasks and all(t.id in passed for t in tasks):
            done = level.number
        else:
            break
    return done


def unlocked_level(store: Store, catalog: Catalog, language: str) -> int:
    return min(completed_levels(store, catalog, language) + 1, catalog.max_level(language))


def is_unlocked(store: Store, catalog: Catalog, task: Task) -> bool:
    """Lessons, dailies and weeklies are all open up to the level you are working on."""
    return task.level <= completed_levels(store, catalog, task.language) + 1


def next_curriculum_task(store: Store, catalog: Catalog, language: str) -> Task | None:
    passed = store.passed_ids()
    level = unlocked_level(store, catalog, language)
    for task in catalog.curriculum(language, level):
        if task.id not in passed:
            return task
    return None


def nothing_unlocked(catalog: Catalog, kind: str, language: str) -> str:
    """Why `journey daily` / `weekly` has nothing to offer, and what to do about it."""
    tasks = catalog.of_kind(language, kind)
    if not tasks:
        return f"There are no {kind} tasks for this track yet."
    lowest = min(t.level for t in tasks)
    return f"{kind.capitalize()} tasks unlock at level {lowest}."


def practice_streak(store: Store, today: date) -> int:
    """Consecutive days, ending today or yesterday, on which you passed something."""
    days = {date.fromtimestamp(ts) for ts in store.completion_timestamps()}
    day = today if today in days else today - timedelta(days=1)
    streak = 0
    while day in days:
        streak += 1
        day -= timedelta(days=1)
    return streak


def passed_on(store: Store, day: date) -> bool:
    return any(date.fromtimestamp(ts) == day for ts in store.completion_timestamps())


def period_key(kind: str, today: date) -> str:
    if kind == "weekly":
        year, week, _ = today.isocalendar()
        return f"{year}-W{week:02d}"
    return today.isoformat()


def pick_task(store: Store, catalog: Catalog, kind: str, language: str, today: date) -> Task | None:
    """The daily (or weekly) task: fixed for the period once chosen, near your rating, unseen."""
    period = period_key(kind, today)
    existing = store.get_pick(period, kind, language)
    if existing and existing in catalog.tasks:
        return catalog.tasks[existing]

    eligible = [t for t in catalog.of_kind(language, kind) if is_unlocked(store, catalog, t)]
    if not eligible:
        return None
    resolved = store.resolved_ids()
    pool = [t for t in eligible if t.id not in resolved] or eligible  # reruns once the pool is dry
    rating, _ = store.rating(language)
    ranked = sorted(pool, key=lambda t: (abs(t.rating - rating), t.id))
    best = abs(ranked[0].rating - rating)
    # Vary the pick only between tasks that fit about equally well.
    similar = [t for t in ranked if abs(t.rating - rating) <= best + 100][:3]
    task = random.Random(f"{period}:{kind}:{language}").choice(similar)
    store.set_pick(period, kind, language, task.id)
    return task
