"""Task packs: what a task is, and how they are loaded from disk.

A task is a directory:

    c01_hello/
        task.toml     metadata, rules and test cases
        subject.md    what the learner reads
        starter/      optional files copied into the workspace (training wheels)
        tests/        optional test harness, never copied to the workspace
        solution/     reference solution, used by `journey validate` and shown after you pass

Levels are described by `<language>/levels.toml`.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from . import config

CONTENT_DIR = Path(__file__).parent / "content"
LANGUAGES = ("c", "python")
KINDS = ("learn", "boss", "daily", "weekly")
RATED_KINDS = ("daily", "weekly")


class TaskError(Exception):
    """A task pack is malformed."""


@dataclass(frozen=True)
class Case:
    name: str
    args: tuple[str, ...] = ()
    stdin: str = ""
    stdout: str = ""
    exit_code: int = 0
    hidden: bool = False
    hint: str = ""  # shown when a hidden case fails
    files: tuple[tuple[str, str], ...] = ()  # fixtures: files created in the working directory
    expect_files: tuple[tuple[str, str], ...] = ()  # files the program must leave behind


@dataclass(frozen=True)
class Rule:
    """A regular expression the solution's source must (or must not) match."""

    pattern: str
    message: str


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    language: str
    kind: str
    level: int
    order: int
    rating: int
    par_minutes: int
    timeout: float
    files: tuple[str, ...]
    allowed: tuple[str, ...]
    cflags: tuple[str, ...]
    ldflags: tuple[str, ...]
    harness: str | None
    forbidden_calls: tuple[str, ...]
    forbidden_imports: tuple[str, ...]
    require: tuple[Rule, ...]
    forbid: tuple[Rule, ...]
    new_skills: tuple[str, ...]
    skills: tuple[str, ...]
    cases: tuple[Case, ...]
    root: Path = field(compare=False)

    @property
    def rated(self) -> bool:
        return self.kind in RATED_KINDS

    @property
    def subject_path(self) -> Path:
        return self.root / "subject.md"

    @property
    def starter_dir(self) -> Path:
        return self.root / "starter"

    @property
    def solution_dir(self) -> Path:
        return self.root / "solution"

    @property
    def provided_dir(self) -> Path:
        """Files the task supplies (a header, a helper module); they overlay the learner's."""
        return self.root / "provided"

    @property
    def harness_path(self) -> Path | None:
        return self.root / self.harness if self.harness else None


@dataclass(frozen=True)
class Level:
    language: str
    number: int
    title: str
    skill: str
    blurb: str


@dataclass
class Catalog:
    tasks: dict[str, Task] = field(default_factory=dict)
    levels: dict[str, list[Level]] = field(default_factory=dict)

    def level(self, language: str, number: int) -> Level | None:
        for lvl in self.levels.get(language, []):
            if lvl.number == number:
                return lvl
        return None

    def max_level(self, language: str) -> int:
        return max((lvl.number for lvl in self.levels.get(language, [])), default=0)

    def curriculum(self, language: str, level: int) -> list[Task]:
        found = [
            t
            for t in self.tasks.values()
            if t.language == language and t.level == level and t.kind in ("learn", "boss")
        ]
        return sorted(found, key=lambda t: (t.order, t.id))

    def of_kind(self, language: str, kind: str) -> list[Task]:
        found = [t for t in self.tasks.values() if t.language == language and t.kind == kind]
        return sorted(found, key=lambda t: (t.level, t.rating, t.id))

    def find(self, text: str) -> Task | None:
        """Exact id, or a unique prefix of one."""
        if text in self.tasks:
            return self.tasks[text]
        matches = [t for tid, t in self.tasks.items() if tid.startswith(text)]
        return matches[0] if len(matches) == 1 else None


def _tuple(data: dict, key: str) -> tuple[str, ...]:
    value = data.get(key, [])
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise TaskError(f"'{key}' must be a list of strings")
    return tuple(value)


def _file_table(case: dict, key: str) -> tuple[tuple[str, str], ...]:
    table = case.get(key, {})
    if not isinstance(table, dict) or not all(isinstance(v, str) for v in table.values()):
        raise TaskError(f"[cases.{key}] must map file names to text")
    for name in table:
        if "/" in name or "\\" in name or name in ("", ".", ".."):
            raise TaskError(f"[cases.{key}] file names must be plain names, not '{name}'")
    return tuple(table.items())


def _rules(data: dict, key: str) -> tuple[Rule, ...]:
    rules = []
    for item in data.get(key, []):
        if "pattern" not in item or "message" not in item:
            raise TaskError(f"every [[{key}]] needs 'pattern' and 'message'")
        rules.append(Rule(item["pattern"], item["message"]))
    return tuple(rules)


def load_task(toml_path: Path) -> Task:
    root = toml_path.parent
    try:
        data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, OSError) as exc:
        raise TaskError(f"{toml_path}: {exc}") from exc
    try:
        task_id = data.get("id", root.name)
        language = data["language"]
        kind = data["kind"]
        if language not in LANGUAGES:
            raise TaskError(f"unknown language '{language}'")
        if kind not in KINDS:
            raise TaskError(f"unknown kind '{kind}'")
        cases = tuple(
            Case(
                name=c["name"],
                args=tuple(c.get("args", [])),
                stdin=c.get("stdin", ""),
                stdout=c.get("stdout", ""),
                exit_code=c.get("exit", 0),
                hidden=c.get("hidden", False),
                hint=c.get("hint", ""),
                files=_file_table(c, "files"),
                expect_files=_file_table(c, "expect_files"),
            )
            for c in data.get("cases", [])
        )
        if not cases:
            raise TaskError("a task needs at least one [[cases]] entry")
        files = _tuple(data, "files")
        if not files:
            raise TaskError("'files' must list the files the learner turns in")
        task = Task(
            id=task_id,
            title=data["title"],
            language=language,
            kind=kind,
            level=int(data["level"]),
            order=int(data.get("order", 50)),
            rating=int(data.get("rating", 800)),
            par_minutes=int(data.get("par_minutes", 15)),
            timeout=float(data.get("timeout", 5)),
            files=files,
            allowed=_tuple(data, "allowed"),
            cflags=_tuple(data, "cflags"),
            ldflags=_tuple(data, "ldflags"),
            harness=data.get("harness"),
            forbidden_calls=_tuple(data, "forbidden_calls"),
            forbidden_imports=_tuple(data, "forbidden_imports"),
            require=_rules(data, "require"),
            forbid=_rules(data, "forbid"),
            new_skills=_tuple(data, "new_skills"),
            skills=_tuple(data, "skills"),
            cases=cases,
            root=root,
        )
    except KeyError as exc:
        raise TaskError(f"{toml_path}: missing required field {exc}") from exc
    except TaskError as exc:
        raise TaskError(f"{toml_path}: {exc}") from exc
    if not task.subject_path.is_file():
        raise TaskError(f"{root}: missing subject.md")
    return task


def _load_levels(path: Path, language: str) -> list[Level]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return [
        Level(language, int(item["number"]), item["title"], item["skill"], item.get("blurb", ""))
        for item in data.get("level", [])
    ]


def _scan(base: Path, catalog: Catalog) -> None:
    if not base.is_dir():
        return
    for toml_path in sorted(base.rglob("task.toml")):
        relative = toml_path.relative_to(base)
        if any(part.startswith((".", "_")) for part in relative.parts[:-1]):
            continue  # work in progress (.wip-<id>) or scratch: not part of the catalog yet
        task = load_task(toml_path)
        if task.id in catalog.tasks:
            raise TaskError(f"duplicate task id '{task.id}' ({toml_path})")
        catalog.tasks[task.id] = task
    for language in LANGUAGES:
        levels_file = base / language / "levels.toml"
        if levels_file.is_file():
            catalog.levels.setdefault(language, []).extend(_load_levels(levels_file, language))


@lru_cache(maxsize=1)
def _cached_catalog(user_dir: str) -> Catalog:
    catalog = Catalog()
    _scan(CONTENT_DIR, catalog)
    _scan(Path(user_dir), catalog)
    for levels in catalog.levels.values():
        levels.sort(key=lambda lvl: lvl.number)
    return catalog


def load_catalog() -> Catalog:
    """Built-in tasks plus anything in `$JOURNEY_HOME/tasks`."""
    return _cached_catalog(str(config.user_tasks_dir()))
