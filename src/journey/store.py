"""All persistent state, in one SQLite file."""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path

from .scoring import START_RATING

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS ratings (
    scope TEXT PRIMARY KEY,
    rating REAL NOT NULL,
    games INTEGER NOT NULL DEFAULT 0
);

-- A task you have started and not finished. Deleted when it is passed or given up.
CREATE TABLE IF NOT EXISTS task_state (
    task_id TEXT PRIMARY KEY,
    started_at REAL NOT NULL,
    active_seconds REAL NOT NULL DEFAULT 0,
    running_since REAL,
    attempts INTEGER NOT NULL DEFAULT 0,
    failed_attempts INTEGER NOT NULL DEFAULT 0,
    repeat INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    ts REAL NOT NULL,
    commit_sha TEXT,
    passed INTEGER NOT NULL,
    active_seconds REAL NOT NULL,
    summary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS completions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    language TEXT NOT NULL,
    kind TEXT NOT NULL,
    ts REAL NOT NULL,
    gave_up INTEGER NOT NULL DEFAULT 0,
    repeat INTEGER NOT NULL DEFAULT 0,
    score REAL NOT NULL,
    stars INTEGER NOT NULL DEFAULT 0,
    active_seconds REAL NOT NULL,
    failed_attempts INTEGER NOT NULL,
    rating_before REAL,
    rating_after REAL,
    expected REAL
);

-- The daily and weekly task chosen for a period, so it stays the same all day or week.
CREATE TABLE IF NOT EXISTS picks (
    period TEXT NOT NULL,
    kind TEXT NOT NULL,
    language TEXT NOT NULL,
    task_id TEXT NOT NULL,
    PRIMARY KEY (period, kind, language)
);
"""


class Store:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path, timeout=10)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self) -> None:
        self.conn.close()

    # -- meta ---------------------------------------------------------------

    def get_meta(self, key: str, default: str | None = None) -> str | None:
        row = self.conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default

    def set_meta(self, key: str, value: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO meta (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value),
            )

    def clear_meta(self, key: str) -> None:
        with self.conn:
            self.conn.execute("DELETE FROM meta WHERE key = ?", (key,))

    # -- ratings ------------------------------------------------------------

    def rating(self, scope: str) -> tuple[float, int]:
        row = self.conn.execute(
            "SELECT rating, games FROM ratings WHERE scope = ?", (scope,)
        ).fetchone()
        return (row["rating"], row["games"]) if row else (START_RATING, 0)

    def set_rating(self, scope: str, rating: float, games: int) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO ratings (scope, rating, games) VALUES (?, ?, ?) "
                "ON CONFLICT(scope) DO UPDATE SET rating = excluded.rating, games = excluded.games",
                (scope, rating, games),
            )

    # -- tasks in progress and the stopwatch ----------------------------------

    def state(self, task_id: str) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM task_state WHERE task_id = ?", (task_id,)
        ).fetchone()

    def states(self) -> list[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM task_state ORDER BY started_at").fetchall()

    def begin(self, task_id: str, now: float, repeat: bool) -> None:
        """Create the task's state (or resume it) and start its stopwatch."""
        with self.conn:
            self.conn.execute(
                "INSERT INTO task_state (task_id, started_at, running_since, repeat) "
                "VALUES (?, ?, ?, ?) "
                "ON CONFLICT(task_id) DO UPDATE SET running_since = COALESCE(running_since, ?)",
                (task_id, now, now, int(repeat), now),
            )

    def settle(self, task_id: str, now: float) -> None:
        """Stop the stopwatch, adding the running stretch to the task's active time."""
        with self.conn:
            self.conn.execute(
                "UPDATE task_state SET active_seconds = active_seconds + (? - running_since), "
                "running_since = NULL WHERE task_id = ? AND running_since IS NOT NULL",
                (now, task_id),
            )

    def settle_all(self, now: float) -> None:
        for row in self.states():
            self.settle(row["task_id"], now)

    def elapsed(self, task_id: str, now: float) -> float:
        row = self.state(task_id)
        if row is None:
            return 0.0
        extra = now - row["running_since"] if row["running_since"] is not None else 0.0
        return row["active_seconds"] + max(0.0, extra)

    def bump_attempt(self, task_id: str, failed: bool) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE task_state SET attempts = attempts + 1, "
                "failed_attempts = failed_attempts + ? WHERE task_id = ?",
                (int(failed), task_id),
            )

    def drop_state(self, task_id: str) -> None:
        with self.conn:
            self.conn.execute("DELETE FROM task_state WHERE task_id = ?", (task_id,))

    # -- history ------------------------------------------------------------

    def add_attempt(
        self, task_id: str, ts: float, commit: str | None, passed: bool, active: float, summary: str
    ) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO attempts (task_id, ts, commit_sha, passed, active_seconds, summary) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (task_id, ts, commit, int(passed), active, summary),
            )

    def add_completion(self, **fields: object) -> None:
        columns = ", ".join(fields)
        marks = ", ".join("?" for _ in fields)
        with self.conn:
            self.conn.execute(
                f"INSERT INTO completions ({columns}) VALUES ({marks})", tuple(fields.values())
            )

    def passed_ids(self) -> set[str]:
        rows = self.conn.execute(
            "SELECT DISTINCT task_id FROM completions WHERE gave_up = 0 AND repeat = 0"
        ).fetchall()
        return {r["task_id"] for r in rows}

    def resolved_ids(self) -> set[str]:
        """Passed or given up; either way, it should not be picked as a daily again."""
        rows = self.conn.execute(
            "SELECT DISTINCT task_id FROM completions WHERE repeat = 0"
        ).fetchall()
        return {r["task_id"] for r in rows}

    def best_stars(self) -> dict[str, int]:
        rows = self.conn.execute(
            "SELECT task_id, MAX(stars) AS best FROM completions WHERE gave_up = 0 GROUP BY task_id"
        ).fetchall()
        return {r["task_id"]: r["best"] for r in rows}

    def completed_since(self, task_id: str, since: float) -> bool:
        """Was the task finished (not given up) at or after the given time?"""
        row = self.conn.execute(
            "SELECT 1 FROM completions WHERE task_id = ? AND gave_up = 0 AND ts >= ? LIMIT 1",
            (task_id, since),
        ).fetchone()
        return row is not None

    def gave_up_since(self, task_id: str, since: float) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM completions WHERE task_id = ? AND gave_up = 1 AND ts >= ? LIMIT 1",
            (task_id, since),
        ).fetchone()
        return row is not None

    def completion_timestamps(self) -> list[float]:
        rows = self.conn.execute("SELECT ts FROM completions WHERE gave_up = 0").fetchall()
        return [r["ts"] for r in rows]

    def recent_completions(self, limit: int) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM completions ORDER BY ts DESC, id DESC LIMIT ?", (limit,)
        ).fetchall()

    def attempts_for(self, task_id: str) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM attempts WHERE task_id = ? ORDER BY ts", (task_id,)
        ).fetchall()

    # -- daily and weekly picks ---------------------------------------------

    def get_pick(self, period: str, kind: str, language: str) -> str | None:
        row = self.conn.execute(
            "SELECT task_id FROM picks WHERE period = ? AND kind = ? AND language = ?",
            (period, kind, language),
        ).fetchone()
        return row["task_id"] if row else None

    def set_pick(self, period: str, kind: str, language: str, task_id: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO picks (period, kind, language, task_id) VALUES (?, ?, ?, ?)",
                (period, kind, language, task_id),
            )


def now() -> float:
    return time.time()
