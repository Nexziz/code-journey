"""Elo and the per-task performance score.

The "opponent" in Elo is the task: every task has a difficulty rating. Finishing a
task gives a performance score between 0 and 1, which plays the role of the match
result. A clean, reasonably fast solve of a task rated equal to you is *expected*
(about 0.76), so you gain rating by beating that and lose it by falling short.
"""

from __future__ import annotations

from dataclasses import dataclass

START_RATING = 800.0
PERFORMANCE_BIAS = 200.0  # a task rated like you is expected to be solved well
PROVISIONAL_GAMES = 10  # bigger rating swings while the rating is still settling

RANKS = (
    (0, "Rookie"),
    (800, "Apprentice"),
    (1000, "Journeyman"),
    (1200, "Adept"),
    (1400, "Expert"),
    (1600, "Master"),
)


def rank_title(rating: float) -> str:
    title = RANKS[0][1]
    for floor, name in RANKS:
        if rating >= floor:
            title = name
    return title


def expected_score(player: float, task: float) -> float:
    return 1.0 / (1.0 + 10 ** ((task - (player + PERFORMANCE_BIAS)) / 400.0))


def k_factor(games: int, kind: str) -> float:
    base = 40.0 if games < PROVISIONAL_GAMES else 24.0
    return base * 1.5 if kind == "weekly" else base


def rating_update(
    player: float, games: int, task_rating: float, score: float, kind: str
) -> tuple[float, float, float]:
    """Return (new_rating, expected_score, delta)."""
    expected = expected_score(player, task_rating)
    delta = k_factor(games, kind) * (score - expected)
    return player + delta, expected, delta


@dataclass(frozen=True)
class Performance:
    score: float
    speed: float | None  # None for learning tasks, which are never timed
    attempts: float
    style: float

    @property
    def stars(self) -> int:
        if self.score >= 0.97:
            return 3
        if self.score >= 0.85:
            return 2
        return 1


def speed_factor(active_seconds: float, par_minutes: float) -> float:
    """1.0 at half the par time or faster, falling linearly to 0.0 at double the par time."""
    ratio = (active_seconds / 60.0) / max(par_minutes, 1.0)
    if ratio <= 0.5:
        return 1.0
    if ratio >= 2.0:
        return 0.0
    return 1.0 - (ratio - 0.5) / 1.5


def attempts_factor(failed_attempts: int) -> float:
    return max(0.0, 1.0 - 0.34 * failed_attempts)


def style_factor(style_issues: int) -> float:
    return max(0.0, 1.0 - 0.25 * min(style_issues, 4))


def performance(
    *,
    rated: bool,
    failed_attempts: int,
    active_seconds: float,
    par_minutes: float,
    style_issues: int,
) -> Performance:
    """Score a *passing* solution.

    Rated tasks (daily and weekly): 0.60 correct + 0.20 speed + 0.10 first try + 0.10 style.
    Learning tasks are never timed: 0.70 correct + 0.20 first try + 0.10 style.
    """
    att = attempts_factor(failed_attempts)
    sty = style_factor(style_issues)
    if rated:
        spd = speed_factor(active_seconds, par_minutes)
        return Performance(0.60 + 0.20 * spd + 0.10 * att + 0.10 * sty, spd, att, sty)
    return Performance(0.70 + 0.20 * att + 0.10 * sty, None, att, sty)
