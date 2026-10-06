"""Pieces shared by the language runners: results, a safe process runner, style and rule checks."""

from __future__ import annotations

import io
import os
import re
import signal
import subprocess
import threading
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

from ..tasks import Case, Task

try:
    import resource
except ImportError:  # Windows has no resource limits
    resource = None

MAX_OUTPUT_BYTES = 1 << 20  # a runaway `while (1) write(...)` must not fill your memory


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""
    hidden: bool = False


@dataclass
class GradeResult:
    checks: list[Check] = field(default_factory=list)
    style: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return bool(self.checks) and all(c.ok for c in self.checks)

    def add(self, name: str, ok: bool, detail: str = "", hidden: bool = False) -> Check:
        check = Check(name, ok, detail, hidden)
        self.checks.append(check)
        return check

    def summary(self) -> str:
        failed = [c.name for c in self.checks if not c.ok]
        total = len(self.checks)
        if not failed:
            return f"passed {total}/{total}"
        return f"failed {len(failed)}/{total}: " + ", ".join(failed[:5])


# -- running programs -------------------------------------------------------------------


@dataclass
class RunOutput:
    stdout: str
    stderr: str
    returncode: int | None
    timed_out: bool = False
    truncated: bool = False


def _limits(cpu_seconds: float):
    if resource is None:
        return None

    def apply() -> None:
        cpu = int(cpu_seconds) + 2
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
        resource.setrlimit(resource.RLIMIT_FSIZE, (16 << 20, 16 << 20))

    return apply


def _kill(proc: subprocess.Popen) -> None:
    try:
        if hasattr(os, "killpg"):
            os.killpg(proc.pid, signal.SIGKILL)
        else:
            proc.kill()
    except (ProcessLookupError, PermissionError, OSError):
        pass


def _pump(stream, buf: bytearray, counter: list[int], on_overflow) -> None:
    try:
        while True:
            chunk = stream.read1(65536)
            if not chunk:
                return
            room = MAX_OUTPUT_BYTES - len(buf)
            if room > 0:
                buf += chunk[:room]
            counter[0] += len(chunk)
            if counter[0] > MAX_OUTPUT_BYTES:
                on_overflow()
    except (OSError, ValueError):
        return


def run_process(
    cmd: list[str],
    *,
    cwd: Path,
    stdin: str = "",
    timeout: float = 5.0,
    env: dict[str, str] | None = None,
) -> RunOutput:
    """Run a command with a timeout, a CPU limit and a cap on how much output it may produce."""
    full_env = {"PATH": os.environ.get("PATH", ""), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    if env:
        full_env.update(env)
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=full_env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            preexec_fn=_limits(timeout),
        )
    except OSError as exc:
        return RunOutput("", f"could not start {cmd[0]}: {exc}", None)

    overflow = threading.Event()

    def on_overflow() -> None:
        if not overflow.is_set():
            overflow.set()
            _kill(proc)

    out_buf, err_buf = bytearray(), bytearray()
    out_n, err_n = [0], [0]
    readers = [
        threading.Thread(
            target=_pump, args=(proc.stdout, out_buf, out_n, on_overflow), daemon=True
        ),
        threading.Thread(
            target=_pump, args=(proc.stderr, err_buf, err_n, on_overflow), daemon=True
        ),
    ]
    for reader in readers:
        reader.start()
    try:
        if proc.stdin:
            proc.stdin.write(stdin.encode())
            proc.stdin.close()
    except (BrokenPipeError, OSError):
        pass

    timed_out = False
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill(proc)
        proc.wait()
    _kill(proc)  # also clears any children the program left behind
    for reader in readers:
        reader.join(timeout=2)
    for pipe in (proc.stdout, proc.stderr):
        if pipe:
            pipe.close()

    return RunOutput(
        stdout=out_buf.decode("utf-8", errors="replace"),
        stderr=err_buf.decode("utf-8", errors="replace"),
        returncode=proc.returncode,
        timed_out=timed_out,
        truncated=overflow.is_set(),
    )


def signal_name(returncode: int | None) -> str:
    if returncode is None or returncode >= 0:
        return ""
    try:
        return signal.Signals(-returncode).name
    except ValueError:
        return f"signal {-returncode}"


# -- text helpers -----------------------------------------------------------------------


def clip(text: str, limit: int = 240) -> str:
    return text if len(text) <= limit else text[:limit] + f"… (+{len(text) - limit} chars)"


def clip_lines(text: str, max_lines: int = 14) -> str:
    lines = text.strip().splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + [f"… ({len(lines) - max_lines} more lines)"]
    return "\n".join(lines)


def describe_args(case: Case) -> str:
    parts = []
    if case.args:
        parts.append("args " + " ".join(repr(a) for a in case.args))
    if case.stdin:
        parts.append("stdin " + repr(clip(case.stdin, 60)))
    return ", ".join(parts)


def compare_output(task: Task, case: Case, out: RunOutput) -> tuple[bool, str]:
    """Judge one finished run. Returns (passed, explanation)."""
    if out.timed_out:
        return False, f"timed out after {task.timeout:g}s (an infinite loop?)"
    if out.truncated:
        return False, "printed far too much output (an infinite loop?)"
    if out.returncode is not None and out.returncode < 0:
        return False, f"crashed with {signal_name(out.returncode)}"
    if out.returncode != case.exit_code:
        return False, f"exit status {out.returncode}, expected {case.exit_code}"
    if out.stdout != case.stdout:
        return False, f"expected {clip(repr(case.stdout))}\n     got {clip(repr(out.stdout))}"
    return True, ""


# -- style and source rules -------------------------------------------------------------

_C_TOKENS = re.compile(r'"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|//[^\n]*|/\*.*?\*/', re.S)


def strip_c_comments(text: str) -> str:
    return _C_TOKENS.sub(lambda m: " " if m.group(0).startswith("/") else m.group(0), text)


def strip_python_comments(text: str) -> str:
    lines = text.split("\n")
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                row, col = tok.start
                lines[row - 1] = lines[row - 1][:col]
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return text
    return "\n".join(lines)


def style_issues(paths: list[Path], max_cols: int) -> list[str]:
    """A deliberately small style check: whitespace and line length."""
    issues = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        if text and not text.endswith("\n"):
            issues.append(f"{path.name}: no newline at the end of the file")
        for number, line in enumerate(text.split("\n"), 1):
            if line != line.rstrip():
                issues.append(f"{path.name}:{number}: trailing whitespace")
            if len(line.expandtabs(4)) > max_cols:
                issues.append(f"{path.name}:{number}: line is longer than {max_cols} columns")
    return issues


def check_rules(task: Task, source: str, result: GradeResult) -> None:
    """Apply the task's [[require]] and [[forbid]] patterns to comment-free source."""
    for rule in task.require:
        found = re.search(rule.pattern, source, re.M) is not None
        result.add(rule.message, found, "" if found else "your code does not do this yet")
    for rule in task.forbid:
        found = re.search(rule.pattern, source, re.M) is not None
        result.add(rule.message, not found, "this is not allowed in this exercise" if found else "")
