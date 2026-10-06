"""Shared test helpers: throwaway task packs and an isolated journey home."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from journey.tasks import Task, load_task


def q(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def make_task(
    root: Path,
    *,
    name: str = "t_task",
    language: str = "python",
    kind: str = "learn",
    level: int = 1,
    order: int = 50,
    rating: int = 800,
    par: int = 10,
    timeout: float = 3,
    files: tuple[str, ...] = ("sol.py",),
    allowed: tuple[str, ...] | None = None,
    cases: list[dict] | None = None,
    require: list[tuple[str, str]] = (),
    forbid: list[tuple[str, str]] = (),
    forbidden_calls: tuple[str, ...] = (),
    forbidden_imports: tuple[str, ...] = (),
    harness: tuple[str, str] | None = None,
) -> Task:
    """Write a minimal task pack under `root` and load it."""
    folder = root / name
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    lines = [
        'title = "Test task"',
        f"language = {q(language)}",
        f"kind = {q(kind)}",
        f"level = {level}",
        f"order = {order}",
        f"rating = {rating}",
        f"par_minutes = {par}",
        f"timeout = {timeout}",
        f"files = {q(list(files))}",
    ]
    if allowed is not None:
        lines.append(f"allowed = {q(list(allowed))}")
    if forbidden_calls:
        lines.append(f"forbidden_calls = {q(list(forbidden_calls))}")
    if forbidden_imports:
        lines.append(f"forbidden_imports = {q(list(forbidden_imports))}")
    if harness:
        lines.append(f"harness = {q('tests/' + harness[0])}")
        (folder / "tests").mkdir()
        (folder / "tests" / harness[0]).write_text(harness[1])
    for pattern, message in require:
        lines += ["[[require]]", f"pattern = {q(pattern)}", f"message = {q(message)}"]
    for pattern, message in forbid:
        lines += ["[[forbid]]", f"pattern = {q(pattern)}", f"message = {q(message)}"]
    for case in cases or [{"name": "default", "stdout": "ok\n"}]:
        lines.append("[[cases]]")
        for key, value in case.items():
            lines.append(f"{key} = {q(value)}")
    (folder / "task.toml").write_text("\n".join(lines) + "\n")
    (folder / "subject.md").write_text("# Test\n")
    return load_task(folder / "task.toml")


def write_files(directory: Path, files: dict[str, str]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (directory / name).write_text(text)
    return directory


class TempDirTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="journey-test-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)


class IsolatedHome(TempDirTestCase):
    """A test case whose journey state and HOME live in a temp directory."""

    def setUp(self) -> None:
        super().setUp()
        patcher = mock.patch.dict(
            os.environ,
            {"HOME": str(self.tmp / "home"), "JOURNEY_HOME": str(self.tmp / "home" / ".journey")},
        )
        (self.tmp / "home").mkdir()
        patcher.start()
        self.addCleanup(patcher.stop)
