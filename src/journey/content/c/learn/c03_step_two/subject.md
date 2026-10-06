# Two at a time

Level 3 · new skill: **loops**

## Assignment

Print the even digits on one line, followed by a newline:

    02468

This time use a `for` loop with an `int` counter that goes up in steps of 2.

## What you need to know

A `for` loop has three parts: start, test, step.

    for (i = 0; i < 10; i = i + 1)

The step can be anything: `i += 2` means `i = i + 2`.

The counter is an `int`, but `write` wants a character. Convert it like in
level 2: `'0' + i`.

## Turn in

- Files: `step_two.c`
- Allowed functions: `write`
