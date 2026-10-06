"""Tiny terminal styling helpers. No dependencies; colour switches off for pipes and NO_COLOR."""

from __future__ import annotations

import os
import sys

_CODES = {
    "bold": "1",
    "dim": "2",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "gray": "90",
}


def color_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("JOURNEY_COLOR") == "1":  # the git hook forces this: git relays the output
        return True
    return sys.stdout.isatty()


def paint(text: str, *styles: str) -> str:
    if not color_enabled() or not styles:
        return text
    codes = ";".join(_CODES[s] for s in styles)
    return f"\033[{codes}m{text}\033[0m"


def ok(text: str) -> str:
    return paint(text, "green")


def bad(text: str) -> str:
    return paint(text, "red")


def warn(text: str) -> str:
    return paint(text, "yellow")


def dim(text: str) -> str:
    return paint(text, "gray")


def bold(text: str) -> str:
    return paint(text, "bold")


def stars(count: int, total: int = 3) -> str:
    return paint("★" * count, "yellow") + dim("☆" * (total - count))


def bar(done: int, total: int, width: int = 12) -> str:
    filled = 0 if total == 0 else round(width * done / total)
    return paint("█" * filled, "green") + dim("░" * (width - filled))


def rule(title: str = "", width: int = 60) -> str:
    if not title:
        return dim("─" * width)
    pad = max(3, width - len(title) - 5)
    return dim("─── ") + bold(title) + " " + dim("─" * pad)


def clock(seconds: float) -> str:
    seconds = max(0, int(seconds))
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


def say(text: str = "") -> None:
    print(text, flush=True)
