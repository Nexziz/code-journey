"""The `journey` command."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime, timedelta
from pathlib import Path

from . import __version__, config, curriculum, engine, gitops, report, runners, ui, validate
from .runners import c as c_runner
from .scoring import PROVISIONAL_GAMES, rank_title
from .store import Store
from .tasks import LANGUAGES, Catalog, Task, TaskError, load_catalog
from .ui import say


class Fail(Exception):
    """A problem to report to the user without a traceback."""


def pretty(path: Path) -> str:
    try:
        return "~/" + str(path.relative_to(Path.home()))
    except ValueError:
        return str(path)


class App:
    def __init__(self) -> None:
        if not config.db_path().exists():
            raise Fail("Journey is not set up yet. Run: journey init")
        self.store = Store(config.db_path())
        self.catalog: Catalog = load_catalog()

    @property
    def language(self) -> str:
        return self.store.get_meta("language", "c") or "c"

    @property
    def workspace(self) -> Path:
        return Path(self.store.get_meta("workspace") or config.default_workspace())

    def current(self) -> Task | None:
        task_id = self.store.get_meta("current")
        if task_id and self.store.state(task_id) and task_id in self.catalog.tasks:
            return self.catalog.tasks[task_id]
        return None

    def target(self, text: str | None, lang: str | None = None) -> Task:
        """Resolve a task id, a unique id prefix, or the words next / daily / weekly."""
        language = lang or self.language
        if text in (None, "next"):
            task = curriculum.next_curriculum_task(self.store, self.catalog, language)
            if task is None:
                raise Fail(
                    f"You have finished the whole {report.language_name(language)} curriculum. "
                    "Try `journey daily` or `journey weekly`."
                )
            return task
        if text in ("daily", "weekly"):
            task = curriculum.pick_task(self.store, self.catalog, text, language, date.today())
            if task is None:
                raise Fail(f"No {text} task is unlocked yet: finish level 1 of the track first.")
            return task
        task = self.catalog.find(text)
        if task is None:
            raise Fail(f"No task called '{text}'. `journey map` lists them.")
        return task

    def active_or(self, text: str | None) -> Task:
        """The task named, or the one you are working on."""
        if text:
            return self.target(text)
        task = self.current()
        if task is None:
            raise Fail("No task in progress. Start one with: journey start")
        return task


# -- journey init -----------------------------------------------------------------------


def cmd_init(args: argparse.Namespace) -> None:
    home = config.home()
    home.mkdir(parents=True, exist_ok=True)
    store = Store(config.db_path())
    workspace = Path(args.workspace).expanduser() if args.workspace else None
    if workspace is None:
        workspace = Path(store.get_meta("workspace") or config.default_workspace())
    store.set_meta("workspace", str(workspace.resolve()))
    store.set_meta("language", args.lang or store.get_meta("language", "c") or "c")

    try:
        remote = config.remote_path()
        gitops.ensure_remote(remote)
        hook = gitops.install_hook(remote, home)
        gitops.ensure_workspace(workspace, remote)
    except gitops.GitError as exc:
        raise Fail(str(exc)) from exc

    lang = store.get_meta("language")
    say(ui.ok("✔ Journey is ready."))
    say()
    say(f"  Workspace   {pretty(workspace)}   {ui.dim('your code lives here; use any editor')}")
    say(f"  Remote      {pretty(remote)}   {ui.dim('your local origin; it grades every push')}")
    say(f"  Hook        {pretty(hook)}")
    say(
        f"  Track       {report.language_name(lang)}   {ui.dim('change it with: journey init --lang python')}"
    )
    say()
    say(ui.bold("Your first steps"))
    say("  journey start          begin the first task and start the stopwatch")
    say("  journey check          try your solution locally (public tests, no score)")
    say('  git add . && git commit -m "done" && git push    turn it in for grading')
    say("  journey status         see your rating, streak and today's tasks")
    say()
    say(ui.dim("Check the setup any time with: journey doctor"))


# -- journey start / subject / check ----------------------------------------------------


def _ensure_task_folder(app: App, task: Task) -> tuple[Path, bool]:
    folder = app.workspace / task.id
    created = not folder.exists()
    folder.mkdir(parents=True, exist_ok=True)
    if task.starter_dir.is_dir():
        for src in task.starter_dir.iterdir():
            if src.is_file() and not (folder / src.name).exists():
                shutil.copy(src, folder / src.name)
    return folder, created


def cmd_start(args: argparse.Namespace) -> None:
    app = App()
    task = app.target(args.task, args.lang)
    if not curriculum.is_unlocked(app.store, app.catalog, task):
        raise Fail(f"{task.id} is locked. `journey map` shows what you need to finish first.")
    passed = task.id in app.store.passed_ids()
    repeat = passed
    if passed and not args.again and args.task not in ("daily", "weekly"):
        raise Fail(f"You already passed {task.id}. Use --again to practise it (rating unchanged).")

    now = time.time()
    app.store.settle_all(now)
    resumed = app.store.state(task.id) is not None
    app.store.begin(task.id, now, repeat)
    app.store.set_meta("current", task.id)
    folder, _ = _ensure_task_folder(app, task)

    level = app.catalog.level(task.language, task.level)
    where = f"Level {task.level}" + (f" · {level.title}" if level else "")
    say(ui.rule(task.id))
    say(ui.dim(f" {task.kind} · {where}"))
    if task.rated:
        say(ui.dim(f" difficulty {task.rating} · par time {task.par_minutes} min"))
    if repeat:
        say(ui.warn(" practice run: your rating will not change"))
    say()
    say(report.render_subject(task))
    say()
    say(ui.rule())
    say(
        f" {'Resumed' if resumed else 'Started'}: the stopwatch is running ({ui.dim('journey pause to stop it')})"
    )
    say(f" Folder:  cd {pretty(folder)}")
    say(f" Files:   {', '.join(task.files)}")
    say(
        ui.dim(' Try it: journey check   ·   Turn in: git add . && git commit -m "..." && git push')
    )


def cmd_subject(args: argparse.Namespace) -> None:
    app = App()
    task = app.active_or(args.task)
    say(report.render_subject(task))


def cmd_check(args: argparse.Namespace) -> None:
    app = App()
    task = app.active_or(args.task)
    folder = app.workspace / task.id
    if not folder.is_dir():
        raise Fail(f"{pretty(folder)} does not exist. Run: journey start {task.id}")
    say(ui.rule(f"check {task.id}"))
    result = runners.grade(task, folder, include_hidden=False)
    for line in report.render_checks(result):
        say(line)
    hidden = sum(1 for c in task.cases if c.hidden)
    say()
    if result.passed:
        say(ui.ok(" ✔ The public checks pass."))
    else:
        say(ui.bad(" ✘ Not passing yet."))
    if hidden:
        say(ui.dim(f" {hidden} hidden test(s) will also run when you push."))
    say(ui.dim(" This was a local check: nothing was recorded."))
    if not result.passed:
        raise SystemExit(1)


def cmd_pause(args: argparse.Namespace) -> None:
    app = App()
    task = app.current()
    if task is None:
        raise Fail("Nothing is running.")
    app.store.settle(task.id, time.time())
    say(
        f"Paused {task.id} at {ui.clock(app.store.elapsed(task.id, time.time()))}. "
        f"Resume with: journey resume"
    )


def cmd_resume(args: argparse.Namespace) -> None:
    app = App()
    task = app.active_or(args.task)
    state = app.store.state(task.id)
    if state is None:
        raise Fail(f"{task.id} is not in progress. Start it with: journey start {task.id}")
    now = time.time()
    app.store.settle_all(now)
    app.store.begin(task.id, now, bool(state["repeat"]))
    app.store.set_meta("current", task.id)
    say(f"Resumed {task.id}; {ui.clock(app.store.elapsed(task.id, now))} on the clock so far.")


def cmd_giveup(args: argparse.Namespace) -> None:
    app = App()
    task = app.active_or(args.task)
    if app.store.state(task.id) is None:
        raise Fail(f"{task.id} is not in progress.")
    if task.rated and not app.store.state(task.id)["repeat"] and not args.yes:
        answer = input(f"Giving up {task.id} counts as a loss for your rating. Continue? [y/N] ")
        if answer.strip().lower() not in ("y", "yes"):
            say("Okay, keep going.")
            return
    change = engine.give_up(app.store, task, time.time())
    if change:
        say(
            f"Gave up {task.id}. {report.language_name(task.language)} rating {change[0]:.0f} → {change[1]:.0f}."
        )
    else:
        say(f"Put {task.id} aside. No penalty; start it again any time.")
    if task.rated:
        say(ui.dim(f"You can now read a model solution: journey solution {task.id}"))


def cmd_solution(args: argparse.Namespace) -> None:
    app = App()
    if args.task:
        task = app.target(args.task)
    else:  # default to whatever you finished last
        recent = app.store.recent_completions(1)
        if not recent:
            raise Fail("Nothing finished yet. Name a task: journey solution <id>")
        task = app.catalog.tasks[recent[0]["task_id"]]
    done = task.id in app.store.resolved_ids()
    if not done:
        raise Fail(
            "Pass the task (or give it up) first; then you can compare with a model solution."
        )
    say(ui.rule(f"model solution · {task.id}"))
    for name in task.files:
        say(ui.bold(name))
        say((task.solution_dir / name).read_text(encoding="utf-8"))
    say(ui.dim("A model solution is one way to do it, not the only way."))


# -- journey status / map / history / daily / weekly -------------------------------------


def _task_status(app: App, task: Task, since: float) -> str:
    if app.store.state(task.id):
        return ui.warn("in progress")
    if app.store.completed_since(task.id, since):
        best = app.store.best_stars().get(task.id, 0)
        return ui.ok("done ") + ui.stars(best)
    if app.store.gave_up_since(task.id, since):
        return ui.dim("given up")
    return "not started"


def _period_start(kind: str, today: date) -> float:
    day = today if kind == "daily" else today - timedelta(days=today.weekday())
    return datetime.combine(day, datetime.min.time()).timestamp()


def _print_pick(app: App, kind: str, lang: str, today: date) -> None:
    label = f" {kind.capitalize():<9}"
    task = curriculum.pick_task(app.store, app.catalog, kind, lang, today)
    if task is None:
        say(f"{label}{ui.dim('unlocks when you finish level 1')}")
        return
    status = _task_status(app, task, _period_start(kind, today))
    say(
        f"{label}{task.id}  {ui.dim(f'rated {task.rating} · par {task.par_minutes} min')}  {status}"
    )


def cmd_status(args: argparse.Namespace) -> None:
    app = App()
    lang = args.lang or app.language
    today, now = date.today(), time.time()
    say(ui.rule("journey"))
    for code in LANGUAGES:
        rating, games = app.store.rating(code)
        if games == 0 and code != lang:
            continue
        note = f"{games} rated task{'s' if games != 1 else ''}"
        if games < PROVISIONAL_GAMES:
            note += f" · provisional until {PROVISIONAL_GAMES}"
        say(f" {report.language_name(code):<9}{rating:<6.0f}{rank_title(rating):<12}{ui.dim(note)}")
    streak = curriculum.practice_streak(app.store, today)
    passed_today = curriculum.passed_on(app.store, today)
    hint = "" if not streak or passed_today else "   (pass a task today to keep it going)"
    say(f" {'Streak':<9}{streak} day{'s' if streak != 1 else ''}" + ui.dim(hint))
    say()

    level_no = curriculum.unlocked_level(app.store, app.catalog, lang)
    level = app.catalog.level(lang, level_no)
    if level:
        tasks = app.catalog.curriculum(lang, level_no)
        passed = app.store.passed_ids()
        done = sum(1 for t in tasks if t.id in passed)
        say(
            f" {'Track':<9}{report.language_name(lang)} · level {level_no}: {level.title}  "
            f"{ui.bar(done, len(tasks), 10)} {done}/{len(tasks)}"
        )
    current = app.current()
    if current:
        running = app.store.state(current.id)["running_since"] is not None
        state = "running" if running else "paused"
        say(
            f" {'Now':<9}{current.id}  {ui.clock(app.store.elapsed(current.id, now))} {ui.dim(state)}"
        )
    for row in app.store.states():
        if current is None or row["task_id"] != current.id:
            say(
                f" {'Paused':<9}{row['task_id']}  {ui.clock(app.store.elapsed(row['task_id'], now))}"
            )
    say()
    _print_pick(app, "daily", lang, today)
    _print_pick(app, "weekly", lang, today)
    say()
    say(ui.dim(" journey start  ·  journey start daily  ·  journey map  ·  journey history"))


def cmd_map(args: argparse.Namespace) -> None:
    app = App()
    languages = LANGUAGES if args.all else (args.lang or app.language,)
    passed = app.store.passed_ids()
    best = app.store.best_stars()
    for lang in languages:
        done_levels = curriculum.completed_levels(app.store, app.catalog, lang)
        say(ui.rule(f"{report.language_name(lang)} track"))
        for level in app.catalog.levels.get(lang, []):
            tasks = app.catalog.curriculum(lang, level.number)
            count = sum(1 for t in tasks if t.id in passed)
            locked = level.number > done_levels + 1
            head = f" Level {level.number}  {level.title}"
            if locked:
                say(ui.dim(f"{head}  🔒 skill: {level.skill}"))
                continue
            marker = ui.ok("✔") if level.number <= done_levels else ui.warn("◀ you are here")
            say(f"{ui.bold(head)}  {ui.bar(count, len(tasks), 8)} {count}/{len(tasks)}  {marker}")
            say(ui.dim(f"   new skill: {level.skill}. {level.blurb}"))
            for task in tasks:
                stars = ui.stars(best[task.id]) if task.id in passed else ui.dim("···")
                tag = ui.dim(" boss") if task.kind == "boss" else ""
                say(f"   {task.id:<28} {stars}{tag}")
        say()


def cmd_history(args: argparse.Namespace) -> None:
    app = App()
    rows = app.store.recent_completions(args.limit)
    if not rows:
        say("Nothing finished yet. Start with: journey start")
        return
    say(ui.rule("recent results"))
    for row in rows:
        when = datetime.fromtimestamp(row["ts"]).strftime("%Y-%m-%d %H:%M")
        outcome = ui.bad("gave up ") if row["gave_up"] else ui.stars(row["stars"]) + " "
        change = ""
        if row["rating_before"] is not None:
            delta = row["rating_after"] - row["rating_before"]
            change = ui.ok(f"{delta:+.0f}") if delta >= 0 else ui.bad(f"{delta:+.0f}")
        elif row["repeat"]:
            change = ui.dim("practice")
        say(
            f" {when}  {row['task_id']:<28} {outcome} {ui.clock(row['active_seconds']):>7}  {change}"
        )


def cmd_daily(args: argparse.Namespace) -> None:
    _show_pick(args, "daily")


def cmd_weekly(args: argparse.Namespace) -> None:
    _show_pick(args, "weekly")


def _show_pick(args: argparse.Namespace, kind: str) -> None:
    app = App()
    lang = args.lang or app.language
    today = date.today()
    task = curriculum.pick_task(app.store, app.catalog, kind, lang, today)
    if task is None:
        say(
            f"No {kind} task is unlocked yet. Finish level 1 of the {report.language_name(lang)} track."
        )
        return
    say(
        ui.rule(
            f"{kind} · {today.isoformat() if kind == 'daily' else curriculum.period_key(kind, today)}"
        )
    )
    say(f" {ui.bold(task.title)}  {ui.dim(task.id)}")
    say(
        ui.dim(
            f" difficulty {task.rating} · about {task.par_minutes} min at par · "
            f"{_task_status(app, task, _period_start(kind, today))}"
        )
    )
    say()
    say(f" Begin with: journey start {kind}")


# -- journey validate / doctor ----------------------------------------------------------


def cmd_validate(args: argparse.Namespace) -> None:
    catalog = load_catalog()
    if args.tasks:
        selected = []
        for text in args.tasks:
            task = catalog.find(text)
            if task is None:
                raise Fail(f"No task called '{text}'.")
            selected.append(task)
    else:
        selected = sorted(
            catalog.tasks.values(), key=lambda t: (t.language, t.level, t.order, t.id)
        )

    failures = 0
    for task in selected:
        started = time.time()
        problems = validate.validate_task(task, catalog)
        took = time.time() - started
        if problems:
            failures += 1
            say(f"{ui.bad('✘')} {task.id}")
            for problem in problems:
                say(f"    {problem}")
        else:
            say(f"{ui.ok('✔')} {task.id}  {ui.dim(f'{took:.1f}s')}")
    if not args.tasks:
        for lang in LANGUAGES:
            for level in catalog.levels.get(lang, []):
                if not catalog.curriculum(lang, level.number):
                    failures += 1
                    say(f"{ui.bad('✘')} {lang} level {level.number} has no tasks")
    say()
    if failures:
        say(ui.bad(f"{failures} problem(s) in {len(selected)} task(s)"))
        raise SystemExit(1)
    say(ui.ok(f"All {len(selected)} task(s) are sound."))


def _doctor_line(good: bool | None, text: str, detail: str = "") -> bool:
    mark = ui.ok("✔") if good else (ui.warn("!") if good is None else ui.bad("✘"))
    say(f" {mark} {text}" + (ui.dim(f"  {detail}") if detail else ""))
    return bool(good)


def cmd_doctor(args: argparse.Namespace) -> None:
    say(ui.rule("doctor"))
    all_ok = True
    _doctor_line(sys.version_info >= (3, 11), f"Python {sys.version.split()[0]}", sys.executable)
    git_path = shutil.which("git")
    all_ok &= _doctor_line(bool(git_path), "git", git_path or "not found: install git")
    cc = c_runner.find_compiler()
    all_ok &= _doctor_line(bool(cc), "C compiler", cc or "not found: install gcc or clang")
    if cc:
        can_san, can_leak = c_runner.sanitizer_support(cc)
        _doctor_line(
            can_san or None,
            "address/undefined sanitizers",
            "" if can_san else "memory errors will not be checked",
        )
        _doctor_line(
            can_leak or None, "leak detection", "" if can_leak else "leaks will not be checked"
        )
    _doctor_line(
        bool(shutil.which("nm")) or None,
        "nm (allowed-functions check)",
        "" if shutil.which("nm") else "that check is skipped",
    )

    say()
    db = config.db_path()
    if not db.exists():
        _doctor_line(False, "journey is not initialised", "run: journey init")
        raise SystemExit(1)
    app = App()
    remote = config.remote_path()
    hook = gitops.hook_path(remote)
    _doctor_line(db.exists(), "state", pretty(config.home()))
    all_ok &= _doctor_line((remote / "HEAD").exists(), "local remote", pretty(remote))
    hook_ok = hook.is_file() and os.access(hook, os.X_OK)
    all_ok &= _doctor_line(
        hook_ok, "grading hook installed", "" if hook_ok else "run: journey init"
    )
    if hook_ok:
        interpreter = hook.read_text().split("exec ")[-1].split()[0].strip("'\"")
        all_ok &= _doctor_line(Path(interpreter).exists(), "hook interpreter", interpreter)
    ws = app.workspace
    origin = (
        gitops.git("remote", "get-url", "origin", cwd=ws, check=False).stdout.strip()
        if (ws / ".git").exists()
        else ""
    )
    all_ok &= _doctor_line(origin == str(remote), "workspace points at the remote", pretty(ws))
    say()
    say(f" {len(app.catalog.tasks)} tasks loaded.")
    if not all_ok:
        raise SystemExit(1)


# -- the git hook -----------------------------------------------------------------------


def _grade_push(app: App, rev: str) -> None:
    task = app.current()
    say(ui.rule("journey"))
    if task is None:
        say(ui.warn(" No task in progress, so nothing was graded."))
        say(ui.dim(" Start one with `journey start`, then push again."))
        return
    now = time.time()
    with tempfile.TemporaryDirectory(prefix="journey-push-") as tmp:
        folder = gitops.export_dir(config.remote_path(), rev, task.id, Path(tmp))
        if folder is None:
            result = runners.GradeResult()
            result.add(
                "Folder turned in",
                False,
                f"'{task.id}/' is not in what you pushed. Did you `git add` it?",
            )
        else:
            result = runners.grade(task, folder, include_hidden=True)
    outcome = engine.submit(app.store, app.catalog, task, result, commit=rev[:7], now=now)
    say(f" Grading {ui.bold(task.id)} at {rev[:7]}  {ui.dim('attempt ' + str(outcome.attempt_no))}")
    say()
    for line in report.render_checks(result):
        say(line)
    for line in report.render_outcome(outcome):
        say(line)
    if outcome.passed:
        nxt = curriculum.next_curriculum_task(app.store, app.catalog, task.language)
        say()
        say(
            ui.dim(
                f" Next: journey start{' ' + nxt.id if nxt else ' daily'}   ·   journey solution {task.id}"
            )
        )


def cmd_hook(args: argparse.Namespace) -> None:
    app = App()
    for line in sys.stdin:
        parts = line.split()
        if len(parts) != 3:
            continue
        _, new, ref = parts
        if set(new) == {"0"}:  # a branch deletion
            continue
        if ref != "refs/heads/main":
            say(ui.warn(f" journey grades pushes to main only; {ref} was not graded."))
            continue
        try:
            _grade_push(app, new)
        except Exception as exc:  # never leave the learner staring at a bare traceback
            say(ui.bad(f" journey could not grade this push: {exc}"))
            say(ui.dim(" Run `journey doctor` to check your setup."))


# -- parser -----------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="journey",
        description="Practise C and Python with ratings, daily tasks and a growing curriculum.",
    )
    parser.add_argument("--version", action="version", version=f"journey {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    def add(name: str, func, help_text: str, *, lang: bool = False):
        p = sub.add_parser(name, help=help_text, description=help_text)
        p.set_defaults(func=func)
        if lang:
            p.add_argument(
                "-l", "--lang", choices=LANGUAGES, help="language track (default: yours)"
            )
        return p

    p = add("init", cmd_init, "set up your workspace, local remote and grading hook")
    p.add_argument("--workspace", help="where your code lives (default ~/journey-workspace)")
    p.add_argument("--lang", choices=LANGUAGES, help="your main track")

    add("status", cmd_status, "your rating, streak, current task and today's tasks", lang=True)
    p = add("start", cmd_start, "start a task: next, daily, weekly, or an id", lang=True)
    p.add_argument("task", nargs="?", help="task id, or next / daily / weekly (default: next)")
    p.add_argument("--again", action="store_true", help="practise a task you already passed")
    p = add("subject", cmd_subject, "show a task's subject again")
    p.add_argument("task", nargs="?")
    p = add("check", cmd_check, "run the public tests on your folder; nothing is recorded")
    p.add_argument("task", nargs="?")
    add("pause", cmd_pause, "stop the stopwatch")
    p = add("resume", cmd_resume, "start the stopwatch again")
    p.add_argument("task", nargs="?")
    p = add("giveup", cmd_giveup, "abandon a task (a loss for rated tasks)")
    p.add_argument("task", nargs="?")
    p.add_argument("-y", "--yes", action="store_true", help="do not ask for confirmation")
    p = add("solution", cmd_solution, "read the model solution of a finished task")
    p.add_argument("task", nargs="?")
    p = add("map", cmd_map, "the levels, the skills they teach, and your stars", lang=True)
    p.add_argument("--all", action="store_true", help="show every language")
    p = add("history", cmd_history, "your recent results")
    p.add_argument("-n", "--limit", type=int, default=15)
    add("daily", cmd_daily, "today's daily task", lang=True)
    add("weekly", cmd_weekly, "this week's task", lang=True)
    p = add("validate", cmd_validate, "check task packs: reference solutions must pass")
    p.add_argument("tasks", nargs="*", help="task ids (default: all)")
    add("doctor", cmd_doctor, "check that everything journey needs is in place")
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["_hook"]:  # internal: the git hook calls this, so it stays out of --help
        cmd_hook(argparse.Namespace())
        return 0
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        args = parser.parse_args(["status"] if config.db_path().exists() else ["init"])
    try:
        args.func(args)
    except Fail as exc:
        print(ui.bad(f"journey: {exc}"), file=sys.stderr)
        return 1
    except TaskError as exc:
        print(ui.bad(f"journey: bad task pack: {exc}"), file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        print(ui.bad(f"journey: {exc}"), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
    return 0
