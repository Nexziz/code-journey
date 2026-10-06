# The next letter

Level 2 · new skill: **variables**

## Assignment

The letter 5 places after `f` in the alphabet is `k`. Do not type it: let the
program work it out.

Store `'f'` in a `char` variable, add 5 to it, then print the variable followed
by a newline. The output must be:

    k

## What you need to know

A variable is a named box for a value:

    int count = 3;          /* a whole number */
    char letter = 'f';      /* one character, written in single quotes */

A `char` is really a small number: `'a'` is 97, so `'a' + 1` is `'b'`. That is
why `letter = letter + 5;` moves you five letters along.

`write` needs an *address*, not the variable itself. `&letter` means "where
letter lives in memory":

    write(1, &letter, 1);   /* send 1 byte, starting at that address */

The compiler complains about variables you declare and never use, and the grader
treats warnings as errors. Use everything you declare.

## Turn in

- Files: `next_letter.c`
- Allowed functions: `write`
