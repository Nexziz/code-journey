# Loud vowels

Level 4 · new skill: **conditions**

## Assignment

Print the alphabet on one line, but write the vowels (`a e i o u`) in capitals,
then a newline:

    AbcdEfghIjklmnOpqrstUvwxyz

## What you need to know

Combine conditions with `||` (or) and `&&` (and):

    if (c == 'a' || c == 'e')

A capital letter is 32 below its lowercase twin, so `c - 32` turns `'a'` into
`'A'`. A neater way to say the same thing is `c - 'a' + 'A'`.

## Turn in

- Files: `vowels.c`
- Allowed functions: `write`
