# Digits, backwards

Level 3 · new skill: **loops**

## Assignment

Print the digits from 9 down to 0 on one line:

    9876543210

## What you need to know

`range` can count in other ways. It takes up to three numbers: where to start,
where to stop (this one is **not** included) and the step.

    range(2, 7)        2 3 4 5 6
    range(0, 10, 2)    0 2 4 6 8
    range(5, 0, -1)    5 4 3 2 1

Mind the stop value: to include 0 when counting down, stop at -1.

## Turn in

- Files: `countdown_digits.py`
