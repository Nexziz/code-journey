# Negative or not

Level 5 · new skill: **functions**

## Assignment

Write a function in `is_negative.py`:

    def is_negative(n):

It **returns** the string `"N"` if `n` is negative, and `"P"` if `n` is positive
or zero. It does not print anything.

## What you need to know

A function is a named piece of code you can call whenever you like:

    def add(a, b):
        return a + b

    total = add(2, 3)       # total is 5

`def` introduces the function, the names in the parentheses are its parameters,
and `return` hands a value back to whoever called it. Everything indented under
the `def` line is the function's body.

From now on exercises ask for **a function in a file**, not a whole program. The
grader has its own little program that imports your function and calls it. So put
only the function in your file: no `input()`, and no `print()` at the top level.

## Turn in

- Files: `is_negative.py`
