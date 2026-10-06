"""Grade a C solution: compile strictly, check allowed functions, then run it under sanitizers."""

from __future__ import annotations

import re
import shutil
import tempfile
from functools import lru_cache
from pathlib import Path

from ..tasks import Task
from .base import (
    GradeResult,
    check_rules,
    clip_lines,
    compare_output,
    describe_args,
    prepare_case_dir,
    run_process,
    strip_c_comments,
    style_issues,
)

STRICT = ["-Wall", "-Wextra", "-Werror", "-Wno-unused-result", "-fno-builtin", "-O0"]
SANITIZE = [
    "-g",
    "-fsanitize=address,undefined",
    "-fno-sanitize-recover=undefined",
    "-fno-omit-frame-pointer",
]
MAX_COLS = 80
SANITIZER_MARKERS = ("ERROR: AddressSanitizer", "ERROR: LeakSanitizer", "runtime error:")


def find_compiler() -> str | None:
    return shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")


@lru_cache(maxsize=1)
def sanitizer_support(cc: str) -> tuple[bool, bool]:
    """Return (can build with sanitizers, leak detection works here)."""
    with tempfile.TemporaryDirectory(prefix="journey-probe-") as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "p.c").write_text(
            "#include <stdlib.h>\nint main(void){char *p = malloc(8); p = 0; return (int)(long)p;}\n"
        )
        build = run_process([cc, *SANITIZE, "p.c", "-o", "p"], cwd=tmp_path, timeout=30)
        if build.returncode != 0:
            return False, False
        run = run_process(["./p"], cwd=tmp_path, env={"ASAN_OPTIONS": "detect_leaks=1"}, timeout=10)
        leaks = "LeakSanitizer" in run.stderr and "fatal error" not in run.stderr
        return True, leaks


def _clean(text: str, *dirs: Path) -> str:
    for directory in dirs:
        text = text.replace(str(directory) + "/", "")
    return text


def _nm(args: list[str], obj: Path, cwd: Path) -> set[str]:
    out = run_process(["nm", *args, "-P", str(obj)], cwd=cwd, timeout=10)
    return {line.split()[0] for line in out.stdout.splitlines() if line.strip()}


def _sanitizer_summary(stderr: str, c_files: list[str]) -> str:
    """Boil a sanitizer report down to the error line and the frames in the learner's own files."""
    keep = []
    for line in stderr.splitlines():
        stripped = line.strip()
        if any(m in stripped for m in SANITIZER_MARKERS) or stripped.startswith("SUMMARY:"):
            keep.append(stripped)
        elif re.match(r"#\d+ ", stripped) and any(f in stripped for f in c_files):
            keep.append(re.sub(r"^(#\d+) 0x[0-9a-f]+ ", r"\1 ", stripped))
    return "\n".join(keep[:7]) or stderr.strip()[:300]


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

    c_files = [f for f in task.files if f.endswith(".c")]
    sources = {f: (workdir / f).read_text(encoding="utf-8", errors="replace") for f in c_files}
    result.style = style_issues([workdir / f for f in c_files], MAX_COLS)

    cc = find_compiler()
    if cc is None:
        result.add("Compiler", False, "no C compiler found; install gcc or clang")
        return result

    stripped = "\n".join(strip_c_comments(text) for text in sources.values())
    if task.harness and re.search(r"\bmain\s*\(", stripped):
        result.add("No main()", False, "this exercise is graded with its own main(); remove yours")
        return result

    with tempfile.TemporaryDirectory(prefix="journey-c-") as tmp:
        tmp_path = Path(tmp)

        # Everything is built from a private copy: the learner's files, then whatever the task
        # provides (a header, say), which wins over a learner's own version.
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        for name in task.files:
            shutil.copy(workdir / name, src_dir / name)
        if task.provided_dir.is_dir():
            for provided in task.provided_dir.iterdir():
                if provided.is_file():
                    shutil.copy(provided, src_dir / provided.name)

        # 1. Compile each file on its own, as strictly as the Norm-style rules demand.
        objects: list[Path] = []
        for name in c_files:
            obj = tmp_path / f"{Path(name).stem}.o"
            build = run_process(
                [cc, *STRICT, *task.cflags, "-I", str(src_dir), "-c", name, "-o", str(obj)],
                cwd=src_dir,
                timeout=30,
            )
            if build.returncode != 0:
                report = clip_lines(_clean(build.stderr or build.stdout, src_dir, workdir))
                result.add("Compilation (-Wall -Wextra -Werror)", False, report)
                return result
            objects.append(obj)
        result.add("Compilation (-Wall -Wextra -Werror)", True)

        # 2. Only the allowed functions may be called.
        if shutil.which("nm"):
            undefined: set[str] = set()
            defined: set[str] = set()
            for obj in objects:
                undefined |= _nm(["-u"], obj, tmp_path)
                defined |= _nm(["--defined-only"], obj, tmp_path)
            used = {s for s in undefined - defined if not s.startswith("_")}
            extra = sorted(used - set(task.allowed) - {"main"})
            allowed_text = ", ".join(task.allowed) if task.allowed else "none"
            result.add(
                f"Allowed functions ({allowed_text})",
                not extra,
                f"you also call: {', '.join(extra)}" if extra else "",
            )
        else:
            result.notes.append("`nm` not found: the allowed-functions check was skipped")

        check_rules(task, stripped, result)

        # 3. Build once with sanitizers (plain if they are unavailable) and run the cases.
        can_sanitize, can_detect_leaks = sanitizer_support(cc)
        flags = list(SANITIZE) if can_sanitize else ["-g"]
        if not can_sanitize:
            result.notes.append(
                "sanitizers unavailable here: memory errors and leaks are not checked"
            )
        elif not can_detect_leaks:
            result.notes.append("leak detection unavailable here: leaks are not checked")
        sources_to_build = [str(src_dir / f) for f in c_files]
        if task.harness_path:
            harness_copy = tmp_path / task.harness_path.name
            shutil.copy(task.harness_path, harness_copy)
            sources_to_build.append(str(harness_copy))
        exe = tmp_path / "prog"
        link = run_process(
            [
                cc,
                "-O0",
                "-fno-builtin",
                "-w",
                *flags,
                *task.cflags,
                "-I",
                str(src_dir),
                *sources_to_build,
                "-o",
                str(exe),
                *task.ldflags,
            ],
            cwd=src_dir,
            timeout=60,
        )
        if link.returncode != 0:
            report = clip_lines(_clean(link.stderr or link.stdout, src_dir, workdir, tmp_path))
            result.add("Linking", False, report)
            return result

        env = {
            "ASAN_OPTIONS": f"detect_leaks={int(can_detect_leaks)}:abort_on_error=0",
            "UBSAN_OPTIONS": "print_stacktrace=1",
        }
        for index, case in enumerate(task.cases):
            if case.hidden and not include_hidden:
                continue
            case_dir = prepare_case_dir(tmp_path, index, case)
            out = run_process(
                [str(exe), *case.args],
                cwd=case_dir,
                stdin=case.stdin,
                timeout=task.timeout,
                env=env,
            )
            if any(marker in out.stderr for marker in SANITIZER_MARKERS):
                label = "hidden test" if case.hidden else case.name
                detail = _clean(_sanitizer_summary(out.stderr, c_files), src_dir, workdir, tmp_path)
                result.add(f"Test: {label}", False, detail, case.hidden)
                continue
            passed, why = compare_output(task, case, out, case_dir)
            if case.hidden:
                result.add(
                    "Hidden test", passed, case.hint or "an edge case you did not cover", True
                )
            else:
                args = describe_args(case)
                detail = why if passed else (f"{args}\n   {why}" if args else why)
                result.add(f"Test: {case.name}", passed, detail)
    return result
