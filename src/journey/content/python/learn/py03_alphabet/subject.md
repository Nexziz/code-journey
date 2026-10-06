# The whole alphabet

Level 3 · new skill: **loops**

## Assignment

Print the lowercase alphabet on one line:

    abcdefghijklmnopqrstuvwxyz

Use a loop. Typing the alphabet into a string is not allowed (the grader checks).

## What you need to know

A `for` loop repeats its indented block once for every value in a sequence.
`range(5)` is the sequence 0, 1, 2, 3, 4:

    for i in range(5):
        print(i)

The indentation is how Python knows what belongs to the loop: four spaces.

`print` ends its line by itself. To stay on the same line, replace the ending:

    print("x", end="")

Print an empty line at the end with `print()`.

## Turn in

- Files: `alphabet.py`
