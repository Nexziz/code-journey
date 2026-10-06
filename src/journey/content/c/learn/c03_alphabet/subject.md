# The whole alphabet

Level 3 · new skill: **loops**

## Assignment

Print the lowercase alphabet on one line, followed by a newline:

    abcdefghijklmnopqrstuvwxyz

Use a loop. Typing the alphabet into a string is not allowed (the grader checks).

## What you need to know

A `while` loop repeats its block for as long as the condition is true. This one
prints the digits `0` to `4`:

    char c = '0';
    while (c <= '4')
    {
        write(1, &c, 1);
        c++;
    }

`c++` means "add 1 to c". Without it the loop would never stop. If a program
ever runs forever, press Ctrl-C.

The same thing written with `for`, which keeps the start, the test and the step
on one line:

    for (c = '0'; c <= '4'; c++)

## Turn in

- Files: `alphabet.c`
- Allowed functions: `write`
