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
            ui.dim("   Fix it and push again. `journey check` tests it locally."),
        ]

    perf = outcome.performance
    assert perf is not None
    failed = outcome.failed_attempts
    detail = ui.clock(outcome.active_seconds)
    if failed:
        detail += f" · {failed} failed {'try' if failed == 1 else 'tries'}"
    lines = ["", f" {ui.ok('✔ PASSED')}  {ui.stars(perf.stars)}  {ui.dim(detail)}"]
    if outcome.rating_after is not None and outcome.rating_before is not None:
        delta = outcome.rating_after - outcome.rating_before
        painted = ui.ok(f"{delta:+.0f}") if delta >= 0 else ui.bad(f"{delta:+.0f}")
        lines.append(
            f"   {language_name(task.language)} {outcome.rating_before:.0f} → "
            f"{ui.bold(f'{outcome.rating_after:.0f}')} ({painted})"
        )
    elif outcome.repeat:
        lines.append(ui.dim("   practice run: your rating is unchanged"))
    if outcome.level_up:
        lines.append(ui.paint(f" ★ Level {outcome.level_up.number} complete", "bold", "yellow"))
    return lines
