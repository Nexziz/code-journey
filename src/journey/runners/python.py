"""Grade a Python solution: syntax, forbidden constructs, then run the test cases."""

from __future__ import annotations

import ast
import shutil
import sys
import tempfile
from pathlib import Path

from ..tasks import Task
from .base import (
    GradeResult,
    check_rules,
    compare_output,
    describe_args,
    run_process,
    strip_python_comments,
    style_issues,
)

MAX_COLS = 100


def _forbidden_constructs(task: Task, tree: ast.AST) -> list[str]:
    """Names from `forbidden_calls` (".sort" means a method) and `forbidden_imports` in use."""
    names = {c for c in task.forbidden_calls if not c.startswith(".")}
    methods = {c[1:] for c in task.forbidden_calls if c.startswith(".")}
    imports = set(task.forbidden_imports)
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in names:
            found.add(node.id)
        elif isinstance(node, ast.Attribute) and node.attr in methods:
            found.add("." + node.attr)
        elif isinstance(node, ast.Import):
            found |= {a.name for a in node.names if a.name.split(".")[0] in imports}
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module
            and node.module.split(".")[0] in imports
        ):
            found.add(node.module)
    return sorted(found)


def grade(task: Task, workdir: Path, *, include_hidden: bool) -> GradeResult:
    result = GradeResult()

    missing = [f for f in task.files if not (workdir / f).is_file()]
    result.add(
        "Files turned in",
        not missing,
        f"missing: {', '.join(missing)}" if missing else ", ".join(task.files),
    )
    if missing:
        return result

    py_files = [f for f in task.files if f.endswith(".py")]
    sources = {f: (workdir / f).read_text(encoding="utf-8", errors="replace") for f in py_files}
    result.style = style_issues([workdir / f for f in py_files], MAX_COLS)

    forbidden: list[str] = []
    for name, text in sources.items():
        try:
            tree = ast.parse(text, filename=name)
        except SyntaxError as exc:
            line = (exc.text or "").strip()
            detail = f"{name}:{exc.lineno}: {exc.msg}" + (f"\n   {line}" if line else "")
            result.add("Syntax", False, detail)
            return result
        forbidden += _forbidden_constructs(task, tree)
    result.add("Syntax", True)

    if task.forbidden_calls or task.forbidden_imports:
        banned = ", ".join(task.forbidden_calls + task.forbidden_imports)
        result.add(
            f"Not using: {banned}",
            not forbidden,
            f"you use: {', '.join(sorted(set(forbidden)))}" if forbidden else "",
        )

    check_rules(task, "\n".join(strip_python_comments(t) for t in sources.values()), result)

    with tempfile.TemporaryDirectory(prefix="journey-py-") as tmp:
        tmp_path = Path(tmp)
        for name in task.files:
            shutil.copy(workdir / name, tmp_path / name)
        entry = py_files[0]
        if task.harness_path:
            shutil.copy(task.harness_path, tmp_path / task.harness_path.name)
            entry = task.harness_path.name

        env = {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}
        for case in task.cases:
            if case.hidden and not include_hidden:
                continue
            out = run_process(
                [sys.executable, entry, *case.args],
                cwd=tmp_path,
                stdin=case.stdin,
                timeout=task.timeout,
                env=env,
            )
            passed, why = compare_output(task, case, out)
            if not passed and out.returncode not in (None, 0) and out.stderr.strip():
                last = out.stderr.strip().splitlines()[-1]
                why = f"{last}\n   (exit status {out.returncode})"
            if case.hidden:
                result.add(
                    "Hidden test", passed, case.hint or "an edge case you did not cover", True
                )
            else:
                args = describe_args(case)
                detail = why if passed else (f"{args}\n   {why}" if args else why)
                result.add(f"Test: {case.name}", passed, detail)
    return result
