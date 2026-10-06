# Digits, backwards

Level 3 · new skill: **loops**

## Assignment

Print the digits from 9 down to 0 on one line, followed by a newline:

    9876543210

Use a loop; the grader rejects a hand-typed `"9876543210"`.

## What you need to know

Loops can count down too. `c--` subtracts 1, and the test changes direction:

    c = '9';
    while (c >= '0')
    {
        ...
        c--;
    }

Be careful with the test: `c > '0'` would stop before printing the `0`.

## Turn in

- Files: `countdown_digits.c`
- Allowed functions: `write`
