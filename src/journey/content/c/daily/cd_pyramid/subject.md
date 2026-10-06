# Build a pyramid

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

## Turn in

- Files: `pyramid.c`
- Allowed functions: `write`
