# code-journey

A command-line trainer for **C** and **Python** with a progressive curriculum, daily and weekly
challenges, and an Elo-style rating. You write code in any editor (VS Code, Vim, anything), and you
hand it in with real git commands, like at 42: `git add`, `git commit`, `git push`. A local grader
checks what you pushed and tells you how it went.

```
$ journey start
─── c01_hello ──────────────────────────────────────────────
 learn · Level 1 · Say something
 ...
$ cd ~/journey-workspace/c01_hello && vim hello.c
$ journey check                       # try it locally, nothing is recorded
$ git add . && git commit -m "hello" && git push
remote: ─── journey ─────────────────────────────────────────
remote:  Grading c01_hello at 037df47  attempt 1
remote:
remote:  ✔ Files turned in  hello.c
remote:  ✔ Compilation (-Wall -Wextra -Werror)
remote:  ✔ Allowed functions (write)
remote:  ✔ Test: prints the greeting
remote:
remote:  ✔ PASSED  ★★★  1.00
```

## Install

You need Python 3.11+, git, and for the C track a C compiler (`gcc` or `clang`). Linux, macOS and
WSL are supported; native Windows is untested.

```sh
git clone https://github.com/Nexziz/code-journey && cd code-journey
python3 -m venv .venv && . .venv/bin/activate
pip install -e .
journey init                 # or: journey init --lang python
journey doctor               # checks git, the compiler, sanitizers and the grading hook
```

`journey init` creates your workspace (`~/journey-workspace`), a private bare repository that acts as
your `origin` (`~/.journey/remote.git`), and a hook that grades every push. State lives in
`~/.journey` (set `JOURNEY_HOME` to move it).

## How it works

1. `journey start` gives you the next task, creates its folder in your workspace and starts a
   stopwatch. The first task of each level usually comes with a skeleton; the rest do not.
2. You write the solution in your editor.
3. `journey check` runs the public tests on your folder without recording anything.
4. `git add`, `git commit`, `git push`. A hook on the local remote grades the commit you pushed and
   git prints the result as `remote:` lines. Forgetting a `git add` is a failed attempt, as at 42.

### Commands

| Command | What it does |
|---|---|
| `journey init` | Set up the workspace, the local remote and the hook. |
| `journey status` | Rating, streak, current task, today's daily and this week's weekly. |
| `journey start [next\|daily\|weekly\|ID]` | Start a task. IDs can be abbreviated to a unique prefix. |
| `journey check [ID]` | Run the public tests locally. Never recorded. |
| `journey pause` / `resume` | Stop and start the stopwatch. |
| `journey subject [ID]` | Read the task description again. |
| `journey giveup [ID]` | Abandon a task. A loss for rated tasks, free for learning tasks. |
| `journey solution [ID]` | Read the model solution of a task you finished. |
| `journey map` | The levels, the skill each one teaches, and your stars. |
| `journey history` | Your recent results. |
| `journey daily` / `weekly` | Show today's or this week's task. |
| `journey validate [ID...]` | Check task packs: model solutions must pass, bad ones must fail. |
| `journey doctor` | Check that everything journey needs is in place. |

## The curriculum

Learning is a Mario-style ladder. Each level introduces **one new skill**, and the tasks of later
levels reuse the earlier ones. Every level ends with a boss task that combines everything so far.
A level unlocks when every task in the previous one is passed.

| Level | C | Python |
|---|---|---|
| 1 | Say something: `write`, `main` | Say something: `print` |
| 2 | Remember things: `int`, `char`, `+ - * / %` | Remember things: `input`, `int`, `//`, `%` |
| 3 | Again and again: `while`, `for` | Again and again: `for`, `range` |
| 4 | Make decisions: `if`, `&&`, `\|\|` | Make decisions: `if`, `elif`, `in` |
| 5 | Name your steps: functions | Name your steps: `def`, `return` |
| 6 | Words and arguments: strings, `argv` | |
| 7 | Point at things: pointers, arrays | |

C starts with `write` only, like at 42, so you meet the machine before the conveniences. The grader
checks which outside functions you call, and tasks can require the new skill (a loop, a `%`) so you
cannot dodge the thing you are meant to practise.

Beyond the ladder there are **daily** tasks (30 to 60 minutes) and **weekly** tasks (about 3
hours). They are picked on the first day or week you ask, close to your rating, and stay the same
for that period. They only use skills from levels you have finished.

## Scoring

Every finished task gets a **performance score** between 0 and 1. Correctness is a gate: nothing
passes without it, and it is worth the most.

| Part | Rated tasks (daily, weekly) | Learning tasks |
|---|---|---|
| Correct (hidden tests too, memory errors and leaks in C) | 0.60 | 0.70 |
| Speed against the task's par time (full marks at half the par time, zero at double) | 0.20 | not timed |
| First try (each failed push costs a third) | 0.10 | 0.20 |
| Style (trailing whitespace, long lines, final newline) | 0.10 | 0.10 |

- **Learning tasks and bosses** give 1 to 3 stars and unlock levels. They never change your rating,
  so you are never afraid to try something new.
- **Daily and weekly tasks** move your **Elo**, one rating per language. Each task has a difficulty
  rating and your score plays the role of the match result. A clean, reasonably fast solve of a task
  rated like you is expected (about 0.76); you gain by beating that and lose by falling short. The
  first 10 rated tasks swing more (provisional), and weeklies count 1.5 times as much.
- Giving up a rated task counts as a loss. A day without practice costs nothing but your streak.
- The stopwatch is wall-clock time between `start` and the passing push, minus time you paused.
  Pause it when you step away. It is an honour system: you are competing against yourself.

## Adding your own tasks

A task is a folder with a `task.toml`, a `subject.md`, a model solution and tests. Put yours in
`~/.journey/tasks/` and they appear next to the built-in ones. `journey validate` proves each task
is sound. See [docs/AUTHORING.md](docs/AUTHORING.md).

## Status and limits

This is an early version (phase 1 of [the plan](docs/DESIGN.md)).

- **60 tasks** today: C has 7 levels (26 tasks), 10 dailies and 2 weeklies; Python has 5 levels
  (15 tasks), 6 dailies and 1 weekly. Once the daily pool is used up, dailies repeat as practice
  runs with no rating change. More content is the main thing still to grow.
- The grader runs your code on your own machine with timeouts, a CPU limit, a cap on output and
  (for C) AddressSanitizer, UBSan and LeakSanitizer. It is not a security sandbox, and the hidden
  tests are readable on your disk.
- Style checking is minimal (whitespace and line length); there is no Norm-style checker yet.
- Elo needs opponents to mean much; with one player it is a motivator more than a measurement.

## Development

```sh
pip install -e . ruff
ruff check src tests && ruff format --check src tests
python -m unittest discover -s tests -t .      # about a minute: it grades every task
journey validate                               # the same content check, with progress
```
