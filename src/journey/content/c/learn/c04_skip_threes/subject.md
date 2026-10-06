# Skip the threes

Level 4 · new skill: **conditions**

## Assignment

Go through the digits 1 to 9. Print the digit itself, except when it is a
multiple of 3: then print `*` instead. End with a newline:

    12*45*78*

## What you need to know

A number is a multiple of 3 when dividing it by 3 leaves no remainder:
`n % 3 == 0`. That is the `%` from level 2 inside the `if` from this level,
inside the loop from level 3. New skills keep stacking on the old ones.

## Turn in

- Files: `skip_threes.c`
- Allowed functions: `write`
