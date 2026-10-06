"""Where journey keeps its state on disk."""

from __future__ import annotations

import os
from pathlib import Path


def home() -> Path:
    """State directory: database, the local git remote, user-made tasks."""
    override = os.environ.get("JOURNEY_HOME")
    return Path(override).expanduser() if override else Path.home() / ".journey"


def db_path() -> Path:
    return home() / "journey.sqlite3"


def remote_path() -> Path:
    """The bare repository you `git push` to. It plays the role of 42's vogsphere."""
    return home() / "remote.git"


def user_tasks_dir() -> Path:
    return home() / "tasks"


def default_workspace() -> Path:
    return Path.home() / "journey-workspace"
