# Build a pyramid

Daily · uses levels 1 to 6

## Assignment

Write a program that takes a number `n` and prints a pyramid of `n` rows. Row `r`
(counting from 1) has `n - r` spaces, then `2 * r - 1` stars, then a newline.
There are no spaces after the stars.

    $ ./pyramid 3
      *
     ***
    *****

For `n` equal to 0, or if the program does not receive exactly one argument, it
prints nothing. `n` is a non-negative integer, at most 50.

## Things to think about

Rows, then two inner loops (spaces, stars). You need to turn the argument into a
number first; digits arrive one character at a time, and each new digit shifts
what you had by a factor of ten.

## Turn in

- Files: `pyramid.c`
- Allowed functions: `write`
