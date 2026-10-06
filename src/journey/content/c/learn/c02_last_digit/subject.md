# The last digit

Level 2 · new skill: **variables**

## Assignment

Store `7 * 8 + 5` in an `int` variable. Print only its **last digit**, followed
by a newline. The output must be:

    1

## What you need to know

`%` gives the remainder of a division: `61 % 10` is `1`, which is the last digit
of 61. The other operators are `+ - * /` (and `/` throws away the remainder:
`61 / 10` is `6`).

To print a digit you need the *character* for it. The digit characters are in
order, so `'0' + 7` is the character `'7'`:

    char c = '0' + 7;

## Turn in

- Files: `last_digit.c`
- Allowed functions: `write`
