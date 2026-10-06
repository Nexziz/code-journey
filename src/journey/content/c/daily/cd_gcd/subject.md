# Greatest common divisor

Daily · uses levels 1 to 6

## Assignment

Write a program that takes two non-negative integers and prints their greatest
common divisor (the largest number that divides both), followed by a newline.

    $ ./gcd 12 18
    6

`gcd(0, n)` is `n`. If the program does not receive exactly two arguments, it
prints only a newline. The arguments are always valid non-negative integers that
fit in an `int`.

## Things to think about

There are two chores here: turning text into numbers, and numbers back into text
(you have no `atoi` and no `printf`). Then the maths: Euclid's algorithm says
that `gcd(a, b)` equals `gcd(b, a % b)`, and you stop when `b` reaches 0.

## Turn in

- Files: `gcd.c`
- Allowed functions: `write`
