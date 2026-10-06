# Design

Why journey works the way it does, and what is planned. Written after the first design discussion;
see the git history for how it evolved.

## Goals

- Practise **C or Python** from absolute beginner upwards, in the terminal.
- Use the **same commands as real work** (`git add`, `git commit`, `git push`), so they become
  habit. The editor is the learner's choice.
- Gamify the *outcome* (rating, stars, streaks), not the typing.
- A **progressive curriculum** in the style of a platformer: one new thing per level, then reuse,
  then combine, then a boss.
- **Daily** (30 to 60 minutes) and **weekly** (about 3 hours) challenges that adapt to the learner.

## Decisions

### Grading goes through real git

A fake `journey add/commit/push` would teach nothing transferable. Instead `journey init` creates a
**local bare repository** as `origin` for a workspace repository, plus a `post-receive` hook. The
hook runs `journey _hook`, which extracts the learner's task folder from the pushed commit and
grades it. Git relays the hook's output as `remote:` lines, so the result appears right after
`git push`, like 42's vogsphere.

Consequences, all intentional: only what is committed counts (a forgotten `git add` is a failed
attempt); only `main` is graded; a push with no task in progress is explained, not recorded.

### One task is "current"

A push grades the current task, the one most recently started or resumed. Starting another pauses
the first. This keeps grading unambiguous and the stopwatch honest: each task has its own clock of
*active* time. `pause` and `resume` exist because wall-clock time while you made tea is not skill.

### What "how you solved it" can mean

Judging style subjectively is out of reach, so the score uses objective signals:

| Signal | How it is measured |
|---|---|
| Correctness | Public and hidden test cases. Exact stdout and exit status. |
| Safety (C) | ASan, UBSan and LeakSanitizer; a finding fails the case. |
| Discipline | `-Wall -Wextra -Werror`; only allowed functions (`nm` on the object files); Python `forbidden_calls` and `forbidden_imports` via `ast`. |
| Practising the skill | `[[require]]` and `[[forbid]]` regular expressions over comment-free source. |
| Speed | Active time against the task's par time. |
| Attempts | Failed pushes. |
| Style | Whitespace and line length. Deliberately small. |

Speed has a modest weight (0.20) so it cannot reward sloppy copy-paste over understanding.

### Elo, adapted

Elo assumes two players. Here the opponent is the **task**, which has a fixed difficulty rating.

- The performance score `S` in [0, 1] plays the match result.
- Expected score `E = 1 / (1 + 10^((task - (player + 200)) / 400))`. The 200-point bias means a
  task rated like you is *expected* to be solved well (E is about 0.76), because a pass is already
  worth at least 0.6.
- `new = old + K (S - E)`, with `K = 40` for the first 10 rated tasks and 24 afterwards, times 1.5
  for weeklies.
- One rating per language. Giving up scores 0. A repeat of a task you passed changes nothing.
- **Learning tasks do not touch the rating.** They award stars and unlock levels. Otherwise a
  rating that can fall would punish exactly the behaviour a learner should have: trying new things.

Honest limits: with a single player and hand-estimated task ratings, Elo is a motivator, not a
measurement. Task ratings should eventually calibrate from real results.

### The curriculum is a ladder with gates

A level is complete when all its learning tasks and its boss are passed; the next level then
unlocks. Dailies and weeklies carry the highest level they need and unlock once those levels are
complete, so they never use a skill the learner has not met. The first task of a level usually
carries a starter skeleton as a gentle on-ramp; the rest start from an empty folder.

### Daily and weekly picks

On the first request in a period, the task is chosen among the unlocked ones the learner has not
resolved, preferring those near their rating (ties inside 100 points are broken by a seeded random
choice) and then stored, so it is stable for the day or ISO week. When the pool is dry, tasks come
back as practice runs.

### Honour system

Hidden tests and reference solutions live on the learner's disk. Anti-cheat would add complexity
and protect nothing: the opponent is yourself. The grader still protects the learner's *machine*
from their own bugs: timeouts, a CPU limit, a cap on output size (a classic beginner mistake is an
infinite `write` loop), and process groups that are killed afterwards.

### Content is plain files

A task is a directory of TOML, Markdown and source files. `journey validate` is the content CI: it
runs reference solutions, starters and deliberately wrong "mutant" solutions through the real
grader. See [AUTHORING.md](AUTHORING.md).

## Roadmap

1. **Done:** the engine, the git loop, the C and Python graders, ratings, 60 tasks.
2. **Next:**
   - skill-level ratings and adaptive picks that favour weak skills, plus spaced review of old
     skills in dailies;
   - generated variants (differential testing against a reference) so one task yields many dailies;
   - multi-file and Makefile weeklies; `malloc` and structs levels for C; more Python levels;
   - a timed exam mode in the style of `examshell`;
   - an optional style checker closer to the 42 Norm.
3. **Later:** shared leaderboards (this needs a server and changes what Elo means), richer stats in
   the terminal.

## Non-goals

A hardened sandbox, anti-cheat, a web UI, or reproducing 42's actual subjects.
