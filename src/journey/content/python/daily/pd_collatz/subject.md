# The Collatz walk

## Assignment

Read a positive whole number `n`. Repeat until `n` is 1:

- if `n` is even, replace it with `n / 2`
- if `n` is odd, replace it with `3 * n + 1`

Print **how many steps** it took. Starting from 6 the walk is
`6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1`: 8 steps.

    $ python3 collatz.py
    6
    8

## Turn in

- Files: `collatz.py`
