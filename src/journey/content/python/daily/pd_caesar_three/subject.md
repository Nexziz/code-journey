# Caesar, wrapping around

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

## Turn in

- Files: `caesar_three.py`
