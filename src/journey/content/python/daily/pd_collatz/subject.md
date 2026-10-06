# The Collatz walk

Daily · uses levels 1 to 4

## Assignment

Read a positive whole number `n`. Repeat until `n` is 1:

- if `n` is even, replace it with `n / 2`
- if `n` is odd, replace it with `3 * n + 1`

Print **how many steps** it took. Starting from 6 the walk is
`6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1`: 8 steps.

    $ python3 collatz.py
    6
    8

## Things to think about

You do not know in advance how many steps there will be, so a `while` loop fits
better than a `for`. Use `//` for the halving so the numbers stay whole.

## Turn in

- Files: `collatz.py`
