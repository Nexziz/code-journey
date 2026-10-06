# Caesar, wrapping around

Daily · uses levels 1 to 2

## Assignment

Julius Caesar is said to have hidden messages by moving every letter a fixed
number of places along the alphabet. Here is a tiny version of that trick.

Read **four lines**: three lowercase letters (`a` to `z`), one per line, and then
a whole number `k` between -1000 and 1000. Move each letter `k` places along the
alphabet and print the three new letters on **one line**, with nothing between
them and in the same order.

The alphabet is a circle. After `z` comes `a` again, and before `a` comes `z`.
`k` can be negative (move backwards), zero (nothing moves) or bigger than 26
(more than one lap).

    $ python3 caesar_three.py
    x
    y
    z
    3
    abc

    $ python3 caesar_three.py
    c
    a
    t
    -3
    zxq

In the second example `c` goes back 3 places to `z`, `a` goes back to `x` and
`t` goes back to `q`. Moving by 26 places, or by -26, brings every letter back
to itself.

## Things to think about

`ord` gives a letter's code, and `ord("a")` is where the alphabet starts, so
`ord(letter) - ord("a")` numbers the letters from 0 (`a`) to 25 (`z`). Wrapping
is easy on a number from 0 to 25. The remainder operator `%` keeps a number
inside a range: `30 % 26` is `4`. In Python, `%` with a positive number on the
right never gives a negative answer, so `-1 % 26` is `25` and going backwards
needs no special case.

You will write the same calculation three times. That is fine at this level.

Do the arithmetic on the letter numbers. Looking letters up in a string that
holds the alphabet (or importing one) is not allowed here: the point is to see
that a letter is just a number that wraps.

## Turn in

- Files: `caesar_three.py`
