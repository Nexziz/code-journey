# Boss: digit by digit

Level 2 · boss

## Assignment

Store `12 * 12 * 12` in an `int` variable, then print the number **one digit at a
time** using `write` (you cannot print a whole number with `write`). Finish with a
newline. The output must be:

    1728

## What you need to know

You have both tools from this level: `/` to cut digits off the right and `%` to
keep only the right-hand part.

    1728 / 1000        is 1
    1728 / 100 % 10    is 7
    1728 / 10 % 10     is 2
    1728 % 10          is 8

Turn each digit into its character by adding `'0'`, as before.

## Turn in

- Files: `digits.c`
- Allowed functions: `write`
