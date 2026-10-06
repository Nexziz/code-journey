# Writing tasks

A task is a directory. Built-in tasks live in `src/journey/content/<language>/`; your own go in
`~/.journey/tasks/` (any depth, anything with a `task.toml` is picked up). Levels are listed in
`<language>/levels.toml`; to add levels of your own, put a `levels.toml` in
`~/.journey/tasks/<language>/`.

```
c05_ft_putchar/
    task.toml      metadata, rules and test cases
    subject.md     what the learner reads
    starter/       optional files copied into the workspace (training wheels)
    tests/         optional test harness, never copied to the workspace
    provided/      optional files the task supplies, such as a header or helper module
    solution/      the reference solution (required)
    mutants/       optional deliberately wrong solutions that must fail
```

Run `journey validate <id>` after every change. It requires that

- the reference solution passes every test, hidden ones included, with no style notes;
- the starter files do **not** pass;
- every mutant **fails**;
- the metadata is sane, and rated tasks that take input have at least one hidden case.

## task.toml

```toml
title = "Print a string"
language = "c"                  # c or python
kind = "learn"                  # learn | boss | daily | weekly
level = 6                       # curriculum level; for daily/weekly: the highest level it needs
order = 2                       # position inside the level (bosses come last)
rating = 790                    # difficulty, on the Elo scale (learners start at 800)
par_minutes = 12                # the pace that earns full speed marks at half of it
timeout = 5                     # seconds per test case (default 5)
files = ["ft_putstr.c"]         # exactly what the learner must turn in
allowed = ["write"]             # C only: outside functions that may be called
harness = "tests/harness.c"     # optional: test program that calls the learner's code
cflags = []                     # C only: extra compiler flags; ldflags for libraries
forbidden_calls = ["len"]       # Python only: names; ".sort" forbids a method
forbidden_imports = ["math"]    # Python only
new_skills = ["strings"]        # shown on the map
skills = ["output", "strings"]

[[require]]                     # a regex the (comment-free) source must match
pattern = "\\b(while|for)\\b"
message = "Uses a loop"

[[forbid]]                      # a regex it must not match
pattern = "abcdefg"
message = "Does not type the alphabet by hand"

[[cases]]
name = "hello"
args = ["hello"]                # command-line arguments
stdin = ""                      # text for standard input
stdout = "hello\n"              # exact expected output
exit = 0                        # expected exit status (default 0)
hidden = false                  # hidden cases run only on push, never in `journey check`
hint = ""                       # shown when a hidden case fails; never reveal the input
```

### Files in, files out

A case can create files before the program runs and check the files it leaves behind. Each case runs
in its own empty directory, so cases never see each other's files. Names must be plain (no `/`).

```toml
[[cases]]
name = "uppercases a file"
args = ["in.txt"]
stdout = "done\n"

[cases.files]                  # fixtures: created in the working directory before the run
"in.txt" = "hello\n"

[cases.expect_files]           # must exist afterwards, with exactly this text
"out.txt" = "HELLO\n"
```

### Provided files

Anything in `provided/` is copied into the learner's folder when they start the task (so their
editor can see a header, say) and is **laid over their files at grading time**. Editing a provided
file therefore changes nothing. Do not list provided files in `files`. Use this for the `struct`
definition that the learner's functions and your harness must agree on:

```
c09_ft_point/provided/ft_point.h      typedef struct s_point { int x; int y; } t_point;
c09_ft_point/tests/harness.c          #include "ft_point.h", then main()
```

Use `[[require]]` so that a task really practises the new skill (a loop, a `%`), and `[[forbid]]` to
catch hard-coded answers. Both are applied after comments are removed, so they cannot be satisfied
by a comment.

## Two kinds of task

**Program tasks** have no `harness`. The learner writes a whole program: a C `main`, or a Python
script that reads `sys.argv` or `input()`. Each case runs it and compares standard output.

**Function tasks** have a `harness`. The learner writes one function, and your harness is a tiny
program that calls it from the command line and prints the result. In C the harness holds `main`
and the learner's file must not (the grader says so). In Python the harness imports the learner's
module by name (`from ft_max import ft_max`).

Keep the harness boring: parse `argv`, call the function, print one line. Tests then read like
`args = ["3", "7"]`, `stdout = "7\n"`. In C, `printf` output is buffered and can appear *after*
output the learner wrote with `write`; when the learner's function prints, let the harness add its
newline with `write` too.

## Writing good tests

- Compute expected output with an **independent** implementation (a few lines of Python), not by
  running the reference solution, or a shared mistake goes unnoticed.
- Public cases teach what the task wants. Hidden cases catch the classic traps: the empty string,
  zero, negative numbers, `INT_MIN`, one element, no arguments, a very long input, ties.
- Make slowness fail when it matters: a hidden case with a huge input and a short `timeout` rejects
  the quadratic solution.
- Avoid output that is not valid UTF-8; the grader decodes output as text.

## Mutants

For each trap you wrote a hidden case for, add a deliberately wrong solution:

```
mutants/int_min_overflow/ft_putnbr.c
mutants/zero_prints_nothing/ft_putnbr.c
```

`journey validate` fails if any mutant passes, which proves the tests catch what you meant them to.
Several built-in tests were tightened this way: a `cd_ft_strstr` without the empty-needle rule
passed until a "both strings empty" case was added, and a Brainfuck interpreter with `int` cells
passed until a test needed the cell to wrap at 256.

## Subjects

A subject is a question, the way an exam at 42 asks one. It has exactly two sections:

- **Assignment**: what to build, precisely. Exact output format (newlines included), inputs and
  their ranges, what happens on bad input, examples, and any limit the hidden tests enforce (for
  example "any `int` must be answered in well under a second"). If a test can fail on it, the
  question must say it.
- **Turn in**: ``- Files: `name` `` and, for C, ``- Allowed functions: ...``. The content tests
  check that every file and allowed function appears.

Leave out everything else: no tutorials, no "what you need to know", no hints, no "things to think
about", no level labels. A learner who needs a concept looks it up (`man 2 write`, the docs). The
test is whether a learner who knows the language could build it from the question alone, without
guessing at the format.

Write original tasks. Taking inspiration from the 42 style is welcome; copying its subjects is not.
