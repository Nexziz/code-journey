"""Turn grades, outcomes and subjects into terminal text."""

from __future__ import annotations

import re

from . import ui
from .engine import Outcome
from .runners import GradeResult
from .tasks import Task

LANGUAGE_NAMES = {"c": "C", "python": "Python"}


def language_name(language: str) -> str:
    return LANGUAGE_NAMES.get(language, language)


_BOLD = re.compile(r"\*\*(.+?)\*\*")
_CODE = re.compile(r"`([^`\n]+)`")


def _inline(line: str) -> str:
    """Bold and code spans, only when colour is on; plain output keeps the raw markdown."""
    if not ui.color_enabled():
        return line
    line = _BOLD.sub(lambda m: ui.bold(m.group(1)), line)
    return _CODE.sub(lambda m: ui.paint(m.group(1), "cyan"), line)


def render_subject(task: Task) -> str:
    out = []
    for line in task.subject_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            out.append(ui.paint(line[2:], "bold", "cyan"))
        elif line.startswith("## "):
            out.append(ui.bold(line[3:]))
        elif line.startswith("    "):
            out.append(ui.paint(line, "cyan"))
        else:
            out.append(_inline(line))
    return "\n".join(out)


def _indent(text: str, prefix: str) -> list[str]:
    return [prefix + line for line in text.splitlines()]


def render_checks(result: GradeResult) -> list[str]:
    lines = []
    for check in result.checks:
        mark = ui.ok("✔") if check.ok else ui.bad("✘")
        lines.append(f" {mark} {check.name}")
        if check.detail and not check.ok:
            lines.extend(_indent(check.detail, "     "))
        elif check.detail and check.ok:
            lines[-1] += ui.dim(f"  {check.detail}")
    if result.style:
        lines.append("")
        lines.append(ui.warn(f" style notes ({len(result.style)}): each costs score, up to 10%"))
        lines.extend(_indent("\n".join(result.style[:5]), "     "))
        if len(result.style) > 5:
            lines.append(f"     … and {len(result.style) - 5} more")
    for note in result.notes:
        lines.append(ui.dim(f" note: {note}"))
    return lines


def render_outcome(outcome: Outcome) -> list[str]:
    task = outcome.task
    if not outcome.passed:
        return [
            "",
            ui.bad(" ✘ Not yet") + f"  (attempt {outcome.attempt_no})",
            ui.dim("   Fix it, then git add / git commit / git push again."),
            ui.dim("   `journey check` runs the public tests on your folder without pushing."),
        ]

    perf = outcome.performance
    assert perf is not None
    lines = ["", f" {ui.ok('✔ PASSED')}  {ui.stars(perf.stars)}  {ui.bold(f'{perf.score:.2f}')}"]
    timing = f"time {ui.clock(outcome.active_seconds)}"
    if task.rated:
        timing += f" (par {ui.clock(task.par_minutes * 60)})"
    failed = outcome.failed_attempts
    first = "first try" if failed == 0 else f"{failed} failed {'try' if failed == 1 else 'tries'}"
    lines.append(ui.dim(f"   {timing} · {first}"))
    if task.rated:
        parts = (
            f"correct 0.60 · speed {0.20 * (perf.speed or 0):.2f} · "
            f"first try {0.10 * perf.attempts:.2f} · style {0.10 * perf.style:.2f}"
        )
    else:
        parts = (
            f"correct 0.70 · first try {0.20 * perf.attempts:.2f} · style {0.10 * perf.style:.2f}"
        )
    lines.append(ui.dim(f"   score: {parts}"))

    name = language_name(task.language)
    if outcome.rating_after is not None and outcome.rating_before is not None:
        delta = outcome.rating_after - outcome.rating_before
        shown = f"{delta:+.0f}"
        painted = ui.ok(shown) if delta >= 0 else ui.bad(shown)
        lines.append(
            f"   {name} rating {outcome.rating_before:.0f} → {ui.bold(f'{outcome.rating_after:.0f}')}"
            f" ({painted})" + ui.dim(f"   expected score was {outcome.expected:.2f}")
        )
    elif outcome.repeat:
        lines.append(ui.dim("   practice run: your best stars are kept, your rating is unchanged"))
    if outcome.level_up:
        lines.append("")
        lines.append(
            ui.paint(
                f" ★ Level {outcome.level_up.number} complete: {outcome.level_up.title}",
                "bold",
                "yellow",
            )
        )
    return lines
