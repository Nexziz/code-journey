# Design

The short version of why journey works the way it does, and where it is going.

## What it should feel like

Type `journey`, pick a number, read a precise question, write the code, push. No setup screens, no
tutorials, no hints, no solutions: like an exam at 42. The question says exactly what to build,
and the rest is up to you.

## How it works

- **A menu, not a manual.** `journey` offers Continue (where you left off), Daily, Weekly and,
  later, Versus. Everything else stays out of the way.
- **Real git.** `journey` creates a workspace and a private bare repository as its `origin`, with
  a `post-receive` hook. On every push to `main` the hook extracts your task folder from the pushed
  commit and grades it. Git prints the result as `remote:` lines. Only what you committed counts.
- **One task at a time.** A push grades the task you started last. Each task has its own stopwatch.
- **A question is a spec.** `subject.md` has an Assignment (exact behaviour, examples, limits) and a
  Turn in list (files, allowed functions). Nothing else.

## Grading

Correctness comes first: public and hidden test cases, exact output. For C also `-Wall -Wextra
-Werror`, the allowed-function list, and AddressSanitizer, UBSan and LeakSanitizer. Tasks can
require a skill (a loop, a `%`) so a hard-coded answer does not pass. A small style check covers
whitespace and line length.

A solved task scores between 0 and 1. For rated tasks (daily, weekly): 0.60 correct, 0.20 speed
against the task's par time, 0.10 first try, 0.10 style. Lessons are never timed: 0.70 correct,
0.20 first try, 0.10 style.

## Ratings

Elo, with the task as the opponent. Each task has a difficulty rating and your score plays the match
result; a clean, reasonably fast solve of a task rated like you is expected (about 0.76). One rating
per language, bigger swings for the first 10 rated tasks, weeklies count 1.5 times. Lessons give
stars and open levels but never change your rating, so trying something new is free.

Daily and weekly tasks are picked near your rating from the levels you have opened, and stay the
same for the day or week.

## Versus (not built yet)

Two players get the same task and the faster correct solution wins; the result moves both ratings
like a chess game. What is feasible, from cheap to expensive:

1. **Ghost race, offline.** The opponent is a bot of a given rating whose finishing time is drawn
   from the task's par time. Same scoring and Elo as a real match, no server, works today.
2. **Challenge a friend, asynchronous.** You send a task id; each plays when they like; times are
   compared and ratings updated. Needs a small shared store (even a git repository would do).
3. **Live match with friends.** A small relay server (WebSocket) does matchmaking and sends both
   players the task at the same moment. Grading stays on each player's machine, so it is trust-based.
4. **Ranked, public.** Tasks and hidden tests must live on the server, and submissions must be graded
   there, which means sandboxing strangers' C code. That is where the real cost and risk are.

## Not goals

A hardened sandbox, anti-cheat for a solo player, a web UI, copying 42's subjects.
