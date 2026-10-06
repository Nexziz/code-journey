# Boss: print any number

Level 5 · boss

## Assignment

Write a function that prints an integer in decimal:

    void ft_putnbr(int nb);

Negative numbers get a leading `-`. No newline. It must work for every `int`,
including the smallest one, `-2147483648`.

## What you need to know

You already know how to peel digits off a number with `/` and `%` (level 2) and
to repeat with a loop (level 3). Two traps remain:

- Digits come out of `%` from the right, but you must print them from the left.
  Find the biggest power of ten that fits first (1, 10, 100, ...), then work
  downwards.
- `-2147483648` has no positive twin: negating it overflows an `int`. Copy the
  number into a `long`, a bigger integer type, before you negate it.

## Turn in

- Files: `ft_putnbr.c`
- Allowed functions: `write`
